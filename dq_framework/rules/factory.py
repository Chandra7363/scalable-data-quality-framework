from .standard import (
    NotNullRule, UniqueRule, RangeRule, AcceptedValuesRule,
    RowCountRule, FreshnessRule, RegexRule
)
from .referential import ReferentialIntegrityRule

RULES = {
    "not_null": NotNullRule,
    "unique": UniqueRule,
    "range": RangeRule,
    "accepted_values": AcceptedValuesRule,
    "row_count": RowCountRule,
    "freshness": FreshnessRule,
    "regex": RegexRule,
    "referential_integrity": ReferentialIntegrityRule,
}

def create_rule(rule_config):
    rule_type = rule_config["type"].lower()
    if rule_type not in RULES:
        raise ValueError(f"Unsupported DQ rule: {rule_type}")
    return RULES[rule_type](rule_config)
