import json
from pathlib import Path

class Reporter:
    def __init__(self, output_path="dq_results.json"):
        self.output_path = Path(output_path)

    def write(self, dataset, results):
        payload = {
            "dataset": dataset,
            "overall_status": "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL",
            "results": results,
        }
        self.output_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

        print(f"\nDataset: {dataset}")
        print("-" * 78)
        print(f"{'Rule':28} {'Status':8} {'Failed':8} Details")
        print("-" * 78)
        for r in results:
            print(f"{r['rule'][:28]:28} {r['status']:8} {r['failed_count']:<8} {r['details']}")
        print("-" * 78)
        print("Overall Status:", payload["overall_status"])
        print("JSON report:", self.output_path)
