"""Run a batch ingestion + parse demo from a log file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> None:
    from ingestion.batch_loader import load_batch_log

    parser = argparse.ArgumentParser(description="Batch ingest and parse access logs.")
    parser.add_argument("--file", required=True, help="Path to log file")
    args = parser.parse_args()

    entries = load_batch_log(args.file)
    print(json.dumps([entry.model_dump() for entry in entries], indent=2))


if __name__ == "__main__":
    main()
