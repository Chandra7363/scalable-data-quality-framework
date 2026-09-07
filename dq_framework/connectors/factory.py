from .csv_connector import CSVConnector
from .database_connector import DatabaseConnector

def create_connector(source):
    source_type = source["type"].lower()
    if source_type == "csv":
        return CSVConnector(source["path"], **source.get("options", {}))
    if source_type in {"database", "sql"}:
        return DatabaseConnector(source["connection_string"], source["query"])
    raise ValueError(f"Unsupported source type: {source_type}")
