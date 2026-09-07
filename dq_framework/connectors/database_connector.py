import pandas as pd
from sqlalchemy import create_engine, text
from .base import BaseConnector

class DatabaseConnector(BaseConnector):
    def __init__(self, connection_string, query):
        self.connection_string = connection_string
        self.query = query

    def read(self):
        engine = create_engine(self.connection_string)
        with engine.connect() as connection:
            return pd.read_sql(text(self.query), connection)
