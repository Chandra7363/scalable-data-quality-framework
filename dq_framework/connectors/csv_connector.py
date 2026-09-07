import pandas as pd
from .base import BaseConnector

class CSVConnector(BaseConnector):
    def __init__(self, path, **kwargs):
        self.path = path
        self.options = kwargs

    def read(self):
        return pd.read_csv(self.path, **self.options)
