from dash import Dash, html
import dash_bootstrap_components as dbc
from rcg_web.code.formatting import container_content

### TODO: add calendar picker and webhooks
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE]
    )
app.title= "Rap Caviar Gender Tracker"
server = app.server

app.layout = dbc.Container(
    [
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

        # full count
        dbc.Row(
            children=container_content['full_count']
        ),

        # bar chart
        html.A(id="plot"),
        dbc.Row(children=container_content['bar_chart'],
            style={'margin':"2rem 0rem"}
            ),

        # full table
        dbc.Row(
            children=container_content['full_table'] 
                ),
            ], style={'margin-top':"2rem"}
    )

if __name__ == "__main__":
    app.run_server()