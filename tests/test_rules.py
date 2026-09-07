import pandas as pd
from dq_framework.rules.standard import NotNullRule, UniqueRule, RangeRule

def test_not_null_rule_detects_null():
    df = pd.DataFrame({"id": [1, None, 3]})
    result = NotNullRule({"type": "not_null", "column": "id"}).validate(df)
    assert result["status"] == "FAIL"
    assert result["failed_count"] == 1

def test_unique_rule_passes():
    df = pd.DataFrame({"id": [1, 2, 3]})
    result = UniqueRule({"type": "unique", "column": "id"}).validate(df)
    assert result["status"] == "PASS"

def test_range_rule_detects_invalid_values():
    df = pd.DataFrame({"age": [18, 30, 101]})
    result = RangeRule({"type": "range", "column": "age", "min": 18, "max": 100}).validate(df)
    assert result["status"] == "FAIL"
    assert result["failed_count"] == 1


def test_regex_rule_detects_invalid_email():
    from dq_framework.rules.standard import RegexRule
    df = pd.DataFrame({"email": ["test@gmail.com", "invalid-email", None]})
    rule = RegexRule({
        "type": "regex", "name": "valid_email", "column": "email",
        "pattern": r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    })
    result = rule.validate(df)
    assert result["status"] == "FAIL"
    assert result["failed_count"] == 2
