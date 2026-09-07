# Scalable Data Quality Framework

A metadata/configuration-driven Python framework for validating multiple datasets and data sources without changing the core execution engine when new datasets or rules are added.

## Design goals
- Configuration-driven: datasets and rules live in YAML.
- Extensible: connectors and DQ rules implement small common interfaces.
- Scalable design: rules can be executed independently and the connector abstraction can be extended to database/cloud sources.
- Auditable: every run produces rule-level PASS/FAIL results and failure counts.
- Testable: rule logic is covered by unit tests.

## Architecture

```text
YAML Configuration
        |
        v
  Config Loader
        |
        v
    DQ Engine
     /     \
    v       v
Connector   Rule Factory
    |           |
    v           v
 CSV / DB     DQ Rules
                |
                v
             Results
                |
                v
      Console / JSON Report
```

The core engine orchestrates execution. It does not contain dataset-specific validation logic.

## Included demonstration
Two datasets are included:
- `customers.csv`
- `orders.csv`

Supported checks:
- not_null
- unique
- range
- accepted_values
- row_count
- freshness
- referential_integrity
- regex (full-string matching; missing values fail)

Connectors:
- CSV
- SQL database via SQLAlchemy

## Run

```bash
pip install -r requirements.txt
python main.py --config configs/customers.yaml
python main.py --config configs/orders.yaml
```

Run tests:

```bash
python -m pytest tests/test_rules.py -v
```

Reports are written to `customer_dq_results.json` and `orders_dq_results.json` respectively.

## Add a new dataset
Create another YAML configuration. No engine code changes are required.

## Add a new rule
Create a class extending `BaseRule` and register it in `dq_framework/rules/factory.py`. Existing rule implementations and engine flow remain unchanged.

## Add a new source
Create a connector implementing `BaseConnector`, then map its source type in the connector factory. This isolates source-specific code from the DQ engine.

## Production extensions
For enterprise scale, the same interfaces can be implemented with Spark/BigQuery/Snowflake connectors, parallel rule execution, a metadata database, incremental/partition-level validation, alerting, orchestration, and historical DQ dashboards.

## Extensibility demonstration
The regex rule was added through `RegexRule`, the rule factory, and YAML metadata. The existing `engine.py` is unchanged. The sample contains one intentionally invalid email. This is a local Pandas demonstration; distributed execution and warehouse pushdown are future extensions, not implemented capabilities.
