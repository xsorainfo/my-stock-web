"""Export config.WATCHLIST with normalized taxonomy fields.

This is an explicit migration aid: it leaves config.py untouched and writes a
reviewable JSON snapshot that can be imported after the catalog is approved.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config import WATCHLIST  # noqa: E402
from taxonomy_utils import normalize_taxonomy, tag_ids_from_raw  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "watchlist_normalized.json",
        help="output JSON path",
    )
    args = parser.parse_args()

    catalog = json.loads((ROOT / "data" / "tag_catalog.json").read_text(encoding="utf-8"))
    result = []
    for item in WATCHLIST:
        normalized = normalize_taxonomy(item)
        normalized["tag_ids"] = tag_ids_from_raw(item.get("tags") or [], catalog)
        enriched = dict(item)
        enriched.update(normalized)
        enriched["taxonomy"] = normalized
        result.append(enriched)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"exported {len(result)} entries to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
