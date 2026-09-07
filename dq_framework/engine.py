from .config_loader import load_config
from .connectors.factory import create_connector
from .rules.factory import create_rule
from .reporting.reporter import Reporter

class DQEngine:
    def __init__(self, config_path):
        self.config = load_config(config_path)
        self.reporter = Reporter(self.config.get("reporting", {}).get("output", "dq_results.json"))

    def run(self):
        connector = create_connector(self.config["source"])
        df = connector.read()
        results = []
        for rule_config in self.config["rules"]:
            try:
                result = create_rule(rule_config).validate(df)
            except Exception as exc:
                result = {
                    "rule": rule_config.get("name", rule_config.get("type", "unknown")),
                    "type": rule_config.get("type", "unknown"),
                    "severity": rule_config.get("severity", "ERROR"),
                    "status": "FAIL",
                    "failed_count": 0,
                    "details": f"Rule execution error: {exc}",
                }
            results.append(result)
        return results

    def report(self, results):
        self.reporter.write(self.config["dataset"], results)
