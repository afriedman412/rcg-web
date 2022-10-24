from dash import Dash, html
import dash_bootstrap_components as dbc
from rcg_web.code.formatting import full_layout
# from rcg_web.code.new_layout import full_layout

### TODO: add calendar picker and webhooks
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE]
    )
app.title= "Rap Caviar Gender Tracker"
server = app.server

app.layout = full_layout

if __name__ == "__main__":
    app.run_server()