from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()
engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])