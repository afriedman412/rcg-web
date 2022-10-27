from dash import Dash
from rcg_web.code.formatting_grid import full_layout

### TODO: add calendar picker and webhooks
app = Dash( __name__)
app.title= "Rap Caviar Gender Tracker"
server = app.server

app.layout = full_layout
if __name__ == "__main__":
    
    app.run_server()