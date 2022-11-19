"""
New version.
"""
from dash import html
from dash.dcc import Markdown, Graph
from .chart_class import Chart
from ..config.config import GENDERS
import logging

class GridMaker:
    def __init__(self):
        self.c = Chart()
        return

    def make_label(self, text: str) -> list:
        return [
                html.H2(
                    [html.A(id=''.join([t.title() for t in text.split()])),
                    html.A(text, href=f"#Top")],
                    className="chart-title"
                )
            ]

    def tally_table(self) -> list:
        table_ = []
        for row in self.c.gender_counts_full:
            logging.debug(row)
            for n, i in enumerate(self.c.gender_indexes):
                logging.debug(f"{n} // {i}")
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

    def chart_table(self) -> list:
        table_ = []
        for row in self.c.chart_w_features:
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

    def bar_charter(self, id_, fig) -> Graph:
        return Graph(
            id=id_, 
            figure=fig, 
            config={
                'staticPlot': True,
                'format': 'svg',
                'displayModeBar': False
                }
            )
    
    @property
    def topline(self) -> list:
        return [
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
                self.c.chart_date,
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
                ], className="spacer"
            )]
    
    @property
    def header_count(self) -> list:
        return [
            html.Div(children=
                    [html.H4(
                        className="site-title",
                        children=[
                            html.Span(f"{d['gender']}: ", className=d['gender'].lower()),
                            f"{d['count']} Credits ({d['pct']}%)"
                            ]) for d in self.c.total_chart_dict],
                    className="spacer"
            )]

    @property
    def bar_charts(self) -> list:
        return [
            html.Div(
                [
                    self.bar_charter('total', self.c.load_plot(False)), 
                    self.bar_charter('pct', self.c.load_plot(True))],
                className="bar-charts"
            )
            ]

    @property
    def tally_cols(self):
        return [
                html.H4(
                    g, className=f"col-head {g.lower()}"
                ) for g in GENDERS
            ]

    @property
    def chart_cols(self) -> list:
        return [
            html.H4(c, className=f"col-head") for c in ['Song', 'Primary Artist', 'Features'] 
        ]

    @property
    def faq(self) -> list:
        return [
        html.Div(
            html.H4(Markdown(open("README.md").readlines())), className="spacer"
            )]


    def full_layout(self) -> html.Div:
        return html.Div(
            className="wrapper",
            children= self.topline + self.header_count + self.bar_charts + self.make_label("Tally") + \
        self.tally_cols + self.tally_table() + self.make_label("Full Chart") + self.chart_cols + self.chart_table() + self.make_label("FAQ") + self.faq
        )