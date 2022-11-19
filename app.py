from dash import Dash
from rcg_web.code.grid_class import GridMaker
import logging
from datetime import datetime as dt
import os

timestamp = dt.strftime(dt.now(), "%Y%m%d")
LOG_PATH = os.path.abspath(f"./rcg_{timestamp}.log")
logging.basicConfig(
        filename=LOG_PATH,
        filemode="a+",
        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
        level=logging.DEBUG
        )


### TODO: add calendar picker and webhooks
app = Dash(__name__, title="Rap Caviar Gender Tracker")
server = app.server

gm = GridMaker()
app.layout = gm.full_layout()

if __name__ == "__main__":
    app.run_server()