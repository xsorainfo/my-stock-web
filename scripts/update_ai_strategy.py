"""Update only the AI strategy report from the latest data snapshot."""
import json
import os
from datetime import datetime

from update_data import generate_ai_strategy_report


DATA_PATH = "data/data.json"


def main():
    with open(DATA_PATH, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    report, meta = generate_ai_strategy_report(
        data.get("stocks", []),
        data.get("macro", []),
        data.get("update_status", {}),
    )
    data["ai_report"] = report
    data["ai_report_meta"] = {
        **meta,
        "updated_at": datetime.now().astimezone().isoformat(),
    }
    with open(DATA_PATH, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
    print("AI策略已更新")


if __name__ == "__main__":
    main()
