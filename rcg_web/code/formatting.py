from .helpers import load_chart, format_features, parse_chart, load_plot, gender_rows_formatter
import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc
from ..config.config import COLORS

full_chart, chart_date = load_chart()
chart_w_features = format_features(full_chart)
total_chart_dict = parse_chart(full_chart)
total_fig, pct_fig = (
    load_plot(full_chart, chart_date, False), 
    load_plot(full_chart, chart_date, True)
    )

gender_rows = {
    g:gender_rows_formatter(g, full_chart) for g in ['Male', 'Female', 'Non-Binary']
}

dt = dash_table.DataTable(
    data=chart_w_features.to_dict('records'),
    columns=[{"name": i, "id": i} for i in chart_w_features.columns],
    fixed_rows={'headers':True},
    style_table={'overflowY': 'scroll', 'height':800},
    style_cell={'textAlign': 'center'},
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
    style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    }
    
)

nav = [
    html.Ul(
        children=[
            html.Li(html.A("Breakdown by artist", href="#Tally")),
            html.Li(html.A("Current chart", href="#Chart")),
            html.Li(html.A("FAQS", href="#FAQ")),
            ]
        )]

count = [
    html.H4(children=[
        html.Span(f"{d['gender']}: ", style={"color":f"{COLORS[d['gender']]}"}),
        html.Span(f"{d['count']} Credits ({d['pct']}%)")],
        style={"margin":"0px"})
        for d in total_chart_dict
    ]

container_content = {
    "title": html.H1(children=[
                    html.A("Rap Caviar", 
                    href="https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd",
                    style={"color":"#1fd362"}
                    ), " Gender Tracker"], 
                style={"color":"#1fd362", "margin-bottom":"0rem"}
                ),
    "date": html.H2(f"{chart_date}", style={
                    "color":"white", "margin-top":"0rem"
                    }),

    "full_count": [
                dbc.Col(
                    html.Div(
                        count,
                        style={'margin-bottom':"2rem"}
                    ), width={"size":True})
            ],

    "bar_chart": [
            dbc.Col(children=[
                    dcc.Graph(
                        id=id_, 
                        figure=fig,
                        config={'staticPlot': True}
                        )], width=6
                    ) for id_, fig in [('total', total_fig), ('pct', pct_fig)]
                ],
    
    "tally": [html.H3(html.A('Tally', href="#top"), className="subheader")] + [
                dbc.Col(children=[
                    html.H4(
                        g, 
                        # className="subheader",
                        style={"color":COLORS[g], "text-align":"center"}
                        ),
                    html.Table(children=gender_rows[g])],width=4) for g in ['Male','Female','Non-Binary']
                ],

    "full_chart": [
        dbc.Col(children=[
            html.H3(html.A('Full Chart', href="#top"), className="subheader"),
            html.Div(dt, style={"margin-top":"2rem"})
        ])
    ]
}

faq = dcc.Markdown('''#### This is the gender balance for today's Spotify [Rap Caviar](https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd) playlist, updated daily at midnight UTC.

#### The purpose of this project is to call attention to the way that, despite the fact that we are in a golden age of female rap, the genre is still dominated by male artists.

#### Non-binary artists are included as well, although their data may only be present if there is a non-binary person on the chart.

#### Rap Caviar is only one of many many Spotify playlists and Spotify is only one of many music outlets, but its prominence still reflects industry trends in a way that I feel makes the point.

#### Genders are inferred automatically from the pronouns on an artist's Last FM and Wikipedia biographies, and manually corrected as needed. If anyone is misgendered, [please let me know!](https://twitter.com/steadynappin_)''')