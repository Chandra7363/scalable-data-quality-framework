from pathlib import Path
import yaml

def load_config(path):
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if not config.get("dataset") or not config.get("source") or not config.get("rules"):
        raise ValueError("Config must contain dataset, source, and rules")
    return config
