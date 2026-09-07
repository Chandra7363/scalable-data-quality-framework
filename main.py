import argparse
from dq_framework.engine import DQEngine

def main():
    parser = argparse.ArgumentParser(description="Configuration-driven Data Quality Framework")
    parser.add_argument("--config", required=True, help="Path to dataset YAML config")
    args = parser.parse_args()

    engine = DQEngine(args.config)
    results = engine.run()
    engine.report(results)

if __name__ == "__main__":
    main()
