"""Run streaming/tail ingestion demo from a log file."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> None:
    from ingestion.stream_loader import tail_file
    from parsing.log_parser import parse_access_log_line

    parser = argparse.ArgumentParser(description="Stream ingest by tailing a log file.")
    parser.add_argument("--file", required=True, help="Path to log file")
    args = parser.parse_args()

    for line in tail_file(args.file):
        parsed = parse_access_log_line(line)
        if parsed:
            print(parsed.model_dump_json())


if __name__ == "__main__":
    main()
