from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from rcg_web.code.helpers import load_chart, load_plot

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE]
    )
server = app.server

full_chart, chart_date = load_chart()
total_fig, pct_fig = (load_plot(full_chart, False), load_plot(full_chart, True))
total_plot, pct_plot = (dcc.Graph(figure=total_fig), dcc.Graph(figure=pct_fig))

app.layout = html.Div(
    [
        html.Div([
            "Rap Caviar Gender Distribution", 
            html.Br(),
            f"Week of {chart_date}"], style={'fontSize':35, 'margin-bottom':"1rem"}
        ),
        html.Div(children=[
            dcc.Graph(id='total', figure=total_fig, className="six columns"),
            dcc.Graph(id='pct', figure=pct_fig, className="six columns"),
        ])
    ], 
    style={"margin": "2rem 10rem 5rem"}
    )

if __name__ == "__main__":
    app.run_server()