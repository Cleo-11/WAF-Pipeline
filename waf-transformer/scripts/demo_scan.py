"""Send a sample request to local /scan endpoint."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> None:
    from utils.io import read_json

    parser = argparse.ArgumentParser(description="Run scan API demo request.")
    parser.add_argument(
        "--api-url",
        default="http://127.0.0.1:8000/scan",
        help="Scan endpoint URL",
    )
    parser.add_argument(
        "--payload-file",
        default=str(ROOT / "sample_data" / "sample_requests.json"),
        help="JSON file containing a list of scan payloads",
    )
    args = parser.parse_args()

    payloads = read_json(args.payload_file)
    first_payload = payloads[0] if isinstance(payloads, list) else payloads
    response = httpx.post(args.api_url, json=first_payload, timeout=10.0)
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    main()
