from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_RUNS_DIR = Path("artifacts/selected-runs")


def summarize_runs(runs_dir: Path) -> list[dict[str, object]]:
    summaries: list[dict[str, object]] = []

    for path in sorted(runs_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue

        summaries.append(
            {
                "path": str(path),
                "item_count": data.get("item_count"),
                "hit_count": data.get("hit_count"),
                "hit_rate": data.get("hit_rate"),
                "top_k": data.get("top_k"),
            }
        )

    return summaries


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize saved JSON eval runs.")
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    args = parser.parse_args()

    for summary in summarize_runs(args.runs_dir):
        print(
            f"{summary['path']}: "
            f"items={summary['item_count']} "
            f"hits={summary['hit_count']} "
            f"hit_rate={summary['hit_rate']} "
            f"top_k={summary['top_k']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
