from dash import html
from dash.dcc import Markdown
from .helpers import load_chart, format_features, parse_chart, gender_rows_df
from ..config.config import GENDERS

full_chart, chart_date = load_chart()
chart_w_features = format_features(full_chart).to_dict('records')
total_chart_dict = parse_chart(full_chart)
gender_rows = gender_rows_df(full_chart)
gender_indexes = list(zip(gender_rows.columns[::2], gender_rows.columns[1::2]))
gender_rows = gender_rows.to_dict('records')

def table_label(text):
    return [
            html.H2(
                [html.A(id=''.join([t.title() for t in text.split()])),
                html.A(text, href=f"#Top")],
                className="chart-title"
            )
        ]

def tally_table():
    table_ = []
    for row in gender_rows:
        for n, i in enumerate(gender_indexes):
            t = html.Div(
                className="grid-item",
                style={
                    "grid-column": f"{n+1}/{n+1}"
                },
                children=[
                    html.Span(
                        row[i[0]],
                        className="tally-artist",
                    ),
                    html.Span(
                        row[i[1]],
                        className="tally-count",
                    ) 
                ] 
            )
            table_.append(t)
    return table_

def chart_table():
    table_ = []
    for row in chart_w_features:
        for n, t in enumerate(['Song', 'Primary Artist', 'Features']):
            t = html.Div(
                html.Span(
                        row[t],
                        className="tally-artist",
                    ),
                className='grid-item',
                style={
                    "grid-column": f"{n+1}/{n+1}"
                }
            )
            table_.append(t)
    return table_
    

topline = [
    html.H1(
            className="site-title s-green",
            children=[
                html.A(id="Top"),
                html.A(
                    "Rap Caviar",
                    href="https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd"
                    ),
                " Gender Tracker"
            ]
        ),
        html.H2(
            chart_date,
            className="site-title",
        ),
        html.Ul(
            children=[
                html.Li(
                    html.A(
                        text, href=anchor
                        )
                ) for anchor, text in zip(
                    ["#Tally", "#FullChart", "#FAQ"],
                    ["Breakdown by artist", "Current chart", "FAQ"]
                    )
            ]
        )]

header_count = [
            html.H4(
                className="site-title",
                children=[
                    html.Span(f"{d['gender']}: ", className=d['gender'].lower()),
                    f"{d['count']} Credits ({d['pct']}%)"
                    ]
                ) for d in total_chart_dict
        ]

tally_cols = [
            html.H4(
                g, className=f"col-head {g.lower()}"
            ) for g in GENDERS
        ]

chart_cols = [
    html.H4(c, className=f"col-head") for c in ['Song', 'Primary Artist', 'Features'] 
]

faq = [
    html.H4(Markdown(open("README.md").readlines()), className="faq")
]

full_layout = html.Div(
    className="wrapper",
    children= topline + header_count + table_label("Tally") + \
        tally_cols + tally_table() + table_label("Full Chart") + chart_cols + chart_table() + table_label("FAQ") + faq
    
    )