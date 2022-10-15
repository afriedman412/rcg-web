from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from rcg_web.code.helpers import load_chart, parse_chart, load_plot, format_features, gender_col_formatter

### TODO: move formatting to another doc
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE]
    )
server = app.server

full_chart, chart_date = load_chart()
chart_w_features = format_features(full_chart)
total_chart_dict = parse_chart(full_chart)
total_fig, pct_fig = (load_plot(full_chart, False), load_plot(full_chart, True))

gcf = []
for g in ['Male', 'Female', 'Non-Binary']:
    gcf += gender_col_formatter(g, full_chart) 
print(gcf)

dt = dash_table.DataTable(
    chart_w_features.to_dict('records'),
    [{"name": i, "id": i} for i in chart_w_features.columns]
)

count = [
    html.H4(
        f"{d['gender']}: {d['count']} Appearances ({d['pct']}%)", style={"margin":"0px"})
        for d in total_chart_dict
    ]

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Rap Caviar Gender Watch", 
                # style={"margin-bottom":"2rem"}
                ),
                width={"size":True}
            )
        ),
        # date
        dbc.Row(
            dbc.Col(
                html.H2(f"{chart_date}", style={"margin-top":"0rem", "margin-bottom":"2rem"}), 
                width={"size":True})
        ),
        # full count
        dbc.Row(
            children=[
                html.A(id="top"),
                dbc.Col(
                    html.Div(
                        count,
                        style={'margin-bottom':"2rem"}
                    ), width={"size":True})
            ]
        ),
        # bar chart
        dbc.Row(children=[
            html.A(id="plot"),
            dbc.Col(
                html.Div(children=[
                    dcc.Graph(
                        id=id_, 
                        figure=fig, 
                        className="six columns", 
                        config={'displayModeBar': False}) 
                        for id_, fig in [('total', total_fig), ('pct', pct_fig)]
                        ]
                    ),
            style={'margin':"2rem 0rem"},
            width={"size":True}
            ),
            ]),
        # full chart
        # dbc.Row(dt, style={'margin-top':"2rem"}),

        # # gender counts
        # dbc.Row(children=[
        #     dbc.Col(html.H5("YYY"), width=3),
        #     dbc.Col(html.H5("6"), width=1)
        #     ]
        # ),
        # dbc.Row(children=[
        #     dbc.Col(html.H5("XXXXX XXXXXXXX XXXXXXX XXXXXXX"), width=3),
        #     dbc.Col(html.H5("633"), width=1)
        #     ]
        # ),

    ],
    style={'margin-top':"2rem"}
    )

if __name__ == "__main__":
    app.run_server()