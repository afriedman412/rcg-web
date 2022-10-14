import datetime as dt
import pandas as pd
import plotly.graph_objects as go
from .. import engine

def load_chart():
    with engine.connect() as conn:
        full_chart = pd.read_sql(
            """
            SELECT chart.song_name, chart.primary_artist_name, chart_date, artist.artist_name, gender
            FROM chart
            INNER JOIN song ON chart.song_spotify_id=song.song_spotify_id
            LEFT JOIN artist ON song.artist_spotify_id=artist.spotify_id
            WHERE chart_date=(SELECT max(chart_date) FROM chart)
            """, conn
            )

    full_chart['gender'] = full_chart['gender'].map({"m": "Male", "f": "Female", "n": "Non-Binary"})
    chart_date = full_chart['chart_date'][0]
    chart_date = dt.datetime.strptime(chart_date, "%Y-%m-%d").strftime("%B %d, %Y")
    return full_chart, chart_date

def load_plot(full_chart, normalize=False):
    count_df = full_chart['gender'].value_counts(normalize=normalize).rename_axis('gender').reset_index(name='count')
    count_df['format'] = 'Percentage' if normalize else 'Total'

    if normalize:
        count_df['count'] = count_df['count'].round(3)*100

    fig = go.Figure(
        go.Bar(
            x=count_df['gender'], y=count_df['count'],
            hovertemplate="<b>%{x}</b>: <br>%{y:.1f}%" if normalize else "<b>%{x}</b>: <br>%{y}",
            text=count_df['count'],
            textposition='outside'
        )
    )
    fig.update_layout(
        title = {
            'text':"% of Total Artist Appearances" if normalize else "Total Artist Appearances",
            'x':0.5,
            'xanchor': 'center'
        },
        yaxis_range=[0,110] if normalize else [0,count_df['count'].max()*1.2],
        margin=dict(t=50, r=20, l=20, b=30),
        paper_bgcolor="LightSteelBlue"
        )

    if normalize:
        fig.update_traces(texttemplate='%{y:.1f}%')

    return fig