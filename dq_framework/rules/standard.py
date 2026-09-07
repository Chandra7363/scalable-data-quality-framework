import pandas as pd
from .base import BaseRule

class NotNullRule(BaseRule):
    def validate(self, df):
        column = self.config["column"]
        failed = int(df[column].isna().sum())
        return self.result(failed == 0, failed, f"{column} must not be null")

class UniqueRule(BaseRule):
    def validate(self, df):
        column = self.config["column"]
        failed = int(df[column].duplicated(keep=False).sum())
        return self.result(failed == 0, failed, f"{column} must be unique")

class RangeRule(BaseRule):
    def validate(self, df):
        column = self.config["column"]
        minimum = self.config.get("min")
        maximum = self.config.get("max")
        valid = pd.Series(True, index=df.index)
        if minimum is not None:
            valid &= df[column] >= minimum
        if maximum is not None:
            valid &= df[column] <= maximum
        failed = int((~valid.fillna(False)).sum())
        return self.result(failed == 0, failed, f"{column} expected in [{minimum}, {maximum}]")

class AcceptedValuesRule(BaseRule):
    def validate(self, df):
        column = self.config["column"]
        values = self.config["values"]
        failed = int((~df[column].isin(values)).sum())
        return self.result(failed == 0, failed, f"{column} allowed values: {values}")

class RowCountRule(BaseRule):
    def validate(self, df):
        minimum = self.config.get("min", 0)
        maximum = self.config.get("max")
        count = len(df)
        passed = count >= minimum and (maximum is None or count <= maximum)
        return self.result(passed, 0 if passed else count, f"row_count={count}")

class FreshnessRule(BaseRule):
    def validate(self, df):
        column = self.config["column"]
        max_age_days = self.config["max_age_days"]
        values = pd.to_datetime(df[column], errors="coerce")
        latest = values.max()
        if pd.isna(latest):
            return self.result(False, len(df), "No valid timestamp found")
        now = pd.Timestamp.now(tz=latest.tz) if latest.tzinfo else pd.Timestamp.now()
        age = (now - latest).total_seconds() / 86400
        return self.result(age <= max_age_days, 0 if age <= max_age_days else 1,
                           f"latest={latest}; age_days={age:.2f}; max={max_age_days}")


class RegexRule(BaseRule):
    """Validate every value against a configured regular expression."""

    def validate(self, df):
        column = self.config["column"]
        pattern = self.config["pattern"]
        valid = df[column].astype("string").str.fullmatch(pattern, na=False)
        failed = int((~valid).sum())
        return self.result(
            failed == 0, failed, f"{column} must match pattern: {pattern}"
        )
