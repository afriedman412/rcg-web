# retooled via this: https://hackersandslackers.com/plotly-dash-with-flask/

from flask import Flask

from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()
engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI']) # TODO: move this where it needs to go

def init_app():
    load_dotenv()
    engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI']) # TODO: move this where it needs to go
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object() # from Tutorial

    with app.app_context():
        # from . import routes # also from Tutorial
        from .code.dashboard import init_dashboard
        app = init_dashboard(app)
        return app
