import pandas as pd
from .base import BaseRule

class ReferentialIntegrityRule(BaseRule):
    def validate(self, df):
        column = self.config["column"]
        reference = self.config["reference"]
        if reference["type"].lower() != "csv":
            raise ValueError("Demo referential rule currently supports CSV references")
        ref_df = pd.read_csv(reference["path"])
        ref_col = reference["column"]
        failed = int((~df[column].isin(ref_df[ref_col])).sum())
        return self.result(failed == 0, failed,
                           f"{column} must exist in {reference['path']}:{ref_col}")
