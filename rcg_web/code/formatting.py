from .helpers import load_chart, format_features, parse_chart, load_plot, gender_rows_df
import dash_bootstrap_components as dbc
from dash import html, dcc
from ..config.config import COLORS, GENDERS

full_chart, chart_date = load_chart()
chart_w_features = format_features(full_chart)
total_chart_dict = parse_chart(full_chart)
total_fig, pct_fig = (
    load_plot(full_chart, chart_date, False), 
    load_plot(full_chart, chart_date, True)
    )

gender_rows = gender_rows_df(full_chart)

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

    "tally": [
        html.H3(html.A('Tally', href="#top"), className="subheader") 
        ] + [
            dbc.Row(
                children=[
                    dbc.Col(html.H4(c, style={
                        "text-align":"center",
                        "color": COLORS[c]
                        })) for c in GENDERS
                ])
        ] + [
                dbc.Row(children=[
                    dbc.Col(children=[
                        html.Span(d[a] if a else "", style={"float":"left"}),
                        html.Span(d[g], style={"float":"right"})
                        ],
                        style={
                            'margin':"0rem 0.5rem",
                            'font-size': "75%",
                            'color': "black",
                            'background-color': "gray" if n%2==0 else "dimgrey",
                            'width': "1fr",
                            },
                            ) for a, g in zip(gender_rows.columns[::2], gender_rows.columns[1::2])
                     
                ],
                style={"justify-content":"center"}
                ) for n, d in enumerate(gender_rows.to_dict('records'))
    ],

    "full_chart": [
        html.H3(html.A('Full Chart', href="#top"), className="subheader") 
        ] + [
            dbc.Row(
                children=[
                    dbc.Col(html.H4(c, style={"text-align":"center"})) for c in ['Song', 'Primary Artist', 'Features']
                ])
    ] + [
            dbc.Row(children=[
                    dbc.Col(
                        html.Span(d[c]), 
                        style={
                            'margin':"0rem 0.5rem",
                            'font-size': "75%",
                            'color': "black",
                            'background-color': "gray" if n%2==0 else "dimgrey"
                            }) for c in ['Song', 'Primary Artist', 'Features']
                     
                ]) for n, d in enumerate(chart_w_features.to_dict('records'))
    ]
}

faq = dcc.Markdown('''#### This is the gender balance for today's Spotify [Rap Caviar](https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd) playlist, updated daily at midnight UTC.

#### The purpose of this project is to call attention to the way that, despite the fact that we are in a golden age of female rap, the genre is still dominated by male artists.

#### Non-binary artists are included as well, although their data may only be present if there is a non-binary person on the chart.

#### Rap Caviar is only one of many many Spotify playlists and Spotify is only one of many music outlets, but its prominence still reflects industry trends in a way that I feel makes the point.

#### Genders are inferred automatically from the pronouns on an artist's Last FM and Wikipedia biographies, and manually corrected as needed. If anyone is misgendered, [please let me know!](https://twitter.com/steadynappin_)''')

full_layout = html.Div(
    children=[
        html.A(id="Top"),
        dbc.Container([  
        dbc.Row(
            dbc.Col(
                container_content['title'],
                width={"size":True}
            ), style={"margin-bottom":"0rem"}
        ),
        # date
        dbc.Row(
            dbc.Col(container_content['date'], 
                width={"size":True})
        ),
        dbc.Row(
            dbc.Col(nav)
        ),

        # count
        html.A(id="Count"),
        dbc.Row(
            children=container_content['full_count']
        ),

        # bar chart
        html.A(id="bar_chart"),
        dbc.Row(children=container_content['bar_chart'],
            style={'margin':"2rem 0rem"}
            ),

        # tally
        html.A(id="Tally"),
        dbc.Row(
        children=container_content['tally'],
            ),
        
        # full chart
        html.A(id="Chart"),
        dbc.Row(
            children=container_content['full_chart'],
            style={'margin':"2rem 0rem"}
        ),

        # FAQ
        html.A(id="FAQ"),
        dbc.Row(
            dbc.Col([
                html.H3(html.A('FAQs', href="#top"), className="subheader"), faq
                ])
        )
            ], style={'margin':"2rem auto"}
        
    )])

