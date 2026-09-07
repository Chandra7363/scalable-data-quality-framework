from abc import ABC, abstractmethod

class BaseRule(ABC):
    def __init__(self, rule_config):
        self.config = rule_config
        self.name = rule_config.get("name", rule_config["type"])
        self.severity = rule_config.get("severity", "ERROR")

    @abstractmethod
    def validate(self, df):
        raise NotImplementedError

    def result(self, passed, failed_count=0, details=""):
        return {
            "rule": self.name,
            "type": self.config["type"],
            "severity": self.severity,
            "status": "PASS" if passed else "FAIL",
            "failed_count": int(failed_count),
            "details": details,
        }
