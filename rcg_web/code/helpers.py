import datetime as dt
import pandas as pd
import plotly.graph_objects as go
from dash import html
import dash_bootstrap_components as dbc
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

def format_features(full_chart):
    features = full_chart.query("primary_artist_name != artist_name").groupby("song_name")['artist_name'].apply(lambda a: ", ".join(a))
    main_chart = full_chart.query("primary_artist_name == artist_name").set_index("song_name")
    chart_w_features = main_chart.drop(['chart_date', 'artist_name', 'gender'],1).join(features).reset_index().rename(columns={'artist_name':'features'})
    return chart_w_features

def parse_chart(full_chart):
    total_df = full_chart['gender'].value_counts().rename_axis('gender').reset_index(name='count')
    pct_df = full_chart['gender'].value_counts(normalize=True).rename_axis('gender').reset_index(name='pct')
    pct_df['pct'] = pct_df['pct'].map(lambda c: c*100).round(2)
    total_df=total_df.set_index('gender').join(pct_df.set_index("gender")).reset_index()
    total_chart_dict = total_df.to_dict("records")
    for k in {'Male', 'Female', 'Non-Binary'}.difference(set([d['gender'] for d in total_chart_dict])):
        total_chart_dict.append({"gender":k, "count":0, "pct":0})
    return total_chart_dict

def gender_col_formatter(g, full_chart):
    l = len(full_chart.query(f"gender=='{g}'"))
    g_list = full_chart.query(f"gender=='{g}'")['artist_name'].value_counts().reset_index().values
    artists = [a[0] for a in g_list]
    counts = [a[1] for a in g_list]
    gender_col = [
        dbc.Col(children=[html.H4(g)] + [html.H6(a) for a in artists], width=3),
        dbc.Col(children=[html.H4(l)] + [html.H6(c) for c in counts], width=1),
        ]
    return gender_col


def load_plot(full_chart, normalize=False):
    count_df = full_chart['gender'].value_counts(normalize=normalize).rename_axis('gender').reset_index(name='count')
    count_df['format'] = 'Percentage' if normalize else 'Total'

    if normalize:
        count_df['count'] = count_df['count'].round(3)*100

    fig = go.Figure(
        go.Bar(
            x=count_df['gender'], y=count_df['count'],
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
        yaxis_range=[0,110] if normalize else [
            0, count_df['count'].max()*1.2 if count_df['count'].max() > 100 else 100],
        margin=dict(t=50, r=20, l=20, b=30),
        paper_bgcolor="white"
        )

    if normalize:
        fig.update_traces(texttemplate='%{y:.1f}%')

    return fig