from dash import Dash
from .grid_class import GridMaker

def init_dashboard(server):
    gm = GridMaker()
    dash_app = Dash(
        server=server, 
        title="Rap Caviar Gender Tracker"
        # routes_pathname_prefix, external_stylesheets also go here
        )
    dash_app.layout = gm.full_layout()
    return dash_app.server