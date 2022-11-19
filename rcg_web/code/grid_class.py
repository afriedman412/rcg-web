"""
Replaces formatting_grid.py/formatting.py
"""
from dash import html
from dash.dcc import Markdown, Graph
from plotly.graph_objects import Figure, Bar
from .chart_class import Chart
from ..config.config import GENDERS, COLORS
import logging

class BarGrapher:
    """
    Splitting this out for easier code nav and consolidation of purpose.

    load_plot from Chart, bar_charter and bar_charts from GridMaker
    """
    def __init__(self, c: Chart):
        self.c = c
        return

    def load_plot(self, normalize: bool=False) -> Figure:
        """
        Creates the bar plot for both total and normalized counts.
        """
        count_df, title = self.c.count_df(normalize)

        fig = Figure(
            Bar(
                x=count_df['gender'], 
                y=count_df['count'],
                marker_color=list(COLORS.values()),
                text=count_df['count'],
                textposition='outside'
            )
        )
        
        fig.update_layout(
            title = {
                'text':title,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'bottom'
            },
            yaxis_range=[0,110] if normalize else [
                0, count_df['count'].max()*1.2],
            margin=dict(t=70, r=20, l=20, b=30),
            paper_bgcolor="white",
            plot_bgcolor="white",
            autosize=True
            )

        if normalize:
            fig.update_traces(texttemplate='%{y:.1f}%')

        return fig

    def bar_charter(self, id_, fig) -> Graph:
        class_name = 'bar-chart l' if id_=='total' else 'bar-chart r'
        return html.Div(Graph(
            id=id_, 
            figure=fig, 
            config={
                'staticPlot': True,
                'format': 'svg',
                'displayModeBar': False
                }
            ), className=class_name)

    @property
    def bar_charts(self) -> list:
        return [
            html.Div(
                [
                    self.bar_charter('total', self.load_plot(False)), 
                    self.bar_charter('pct', self.load_plot(True))],
                className="bar-chart-container"
            )
            ]

class GridMaker:
    """
    For laying out the data on the page.
    """
    def __init__(self, date: str=None):
        self.set_date(date)
        return

    def set_date(self, date: str=None):
        self.c = Chart(date)
        self.bg = BarGrapher(self.c)
        return

    def full_layout(self, date: str=None) -> html.Div:
        if date:
            self.set_date(date)
        children = []
        for c in [
            self.topline, 
            self.header_count, 
            self.bg.bar_charts, 
            self.make_label("Tally"),
            self.tally_cols, 
            self.tally_table(), 
            self.make_label("Full Chart"),
            self.chart_cols,
            self.chart_table(),
            self.make_label("FAQ"),
            self.faq
            ]:
                children += c
        return html.Div(className="wrapper", children = children)

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
                        ["#Tally", "#FullChart", "#Faq"],
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

    def make_label(self, text: str) -> list:
        return [
                html.H2(
                    [html.A(id=''.join([t.title() for t in text.split()])),
                    html.A(text, href=f"#Top")],
                    className="chart-title"
                )
            ]

    @property
    def tally_cols(self) -> list:
        return [
                html.H4(
                    g, className=f"col-head {g.lower()}"
                ) for g in GENDERS
            ]

    def tally_table(self) -> list:
        table_ = []
        for r, row in enumerate(self.c.gender_counts_full):
            logging.debug(row)
            for n, i in enumerate(self.c.gender_indexes):
                logging.debug(f"{n} // {i}")
                class_name = "grid-item even" if r % 2 else "grid-item odd"
                t = html.Div(
                    className=class_name,
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

    @property
    def chart_cols(self) -> list:
        return [
            html.H4(c, className=f"col-head") for c in ['Song', 'Primary Artist', 'Features'] 
        ]

    def chart_table(self) -> list:
        table_ = []
        for r, row in enumerate(self.c.chart_w_features):
            class_name = "grid-item even" if r % 2 else "grid-item odd"
            for n, t in enumerate(['Song', 'Primary Artist', 'Features']):
                t = html.Div(
                    html.Span(
                            row[t],
                            className="tally-artist",
                        ),
                    className=class_name,
                    style={
                        "grid-column": f"{n+1}/{n+1}"
                    }
                )
                table_.append(t)
        return table_

    @property
    def faq(self) -> list:
        return [
        html.Div(
            html.H4(Markdown(open("README.md").readlines())), className="spacer"
            )]