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
    chart_w_features.to_dict('records'),
    [{"name": i, "id": i} for i in chart_w_features.columns]
)

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
            html.A(id="top"),
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
    
    "full_table": [
                dbc.Col(children=[
                    html.H5(
                        g, 
                        className="subheader",
                        style={"color":COLORS[g]}
                        ),
                    html.Table(children=gender_rows[g])],width=4) for g in ['Male','Female','Non-Binary']
                ]
    
    
}