import json
import re
from urllib.parse import parse_qsl

INPUT_FILE = "../data/raw_requests.jsonl"
OUTPUT_FILE = "../data/train.txt"

KEEP_PREFIXES = [
    "/rest/products",
    "/rest/user",
    "/api/Products",
    "/api/Challenges",
    "/api/Quantitys",
    "/rest/languages",
    "/profile",
    "/rest/basket",
    "rest/chatbot",
    "/api/Users",
    "/api/SecurityQuestions",
    "/api/SecurityAnswers",
    "/api/BasketItems",
    "/api/Deliverys",
    "/api/Cards",
]

DROP_PREFIXES = [
    "/rest/admin",
    "/assets",
    "/media",
    "/socket.io",
]

DROP_SUFFIXES = [
    ".css",
    ".js",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".woff",
    ".woff2",
    ".ico",
    ".map",
]


def should_keep(path: str) -> bool:
    if not path:
        return False

    for prefix in DROP_PREFIXES:
        if path.startswith(prefix):
            return False

    for suffix in DROP_SUFFIXES:
        if path.endswith(suffix):
            return False

    for prefix in KEEP_PREFIXES:
        if path.startswith(prefix):
            return True

    return False


def normalize_path(path: str) -> str:
    path = re.sub(r"/\d+(/|$)", r"/NUM\1", path)
    path = re.sub(r"/+", "/", path)
    return path


def normalize_value(value: str) -> str:
    value = str(value).strip()

    if value == "":
        return "EMPTY"

    if re.fullmatch(r"\d+", value):
        return "NUM"

    if re.fullmatch(r"\d+\.\d+", value):
        return "FLOAT"

    if re.fullmatch(r"[0-9a-fA-F-]{36}", value):
        return "UUID"

    if re.fullmatch(r"[\w\.-]+@[\w\.-]+\.\w+", value):
        return "EMAIL"

    if re.fullmatch(r"[A-Fa-f0-9]{16,}", value):
        return "HEX"

    # JWT-like / very long token-ish strings
    if len(value) > 80:
        return "LONGTEXT"

    return "TEXT"


def clean_key(key: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", str(key))


def add_query_tokens(tokens: list[str], query: str) -> None:
    for key, value in parse_qsl(query, keep_blank_values=True):
        key = clean_key(key)
        if not key:
            continue
        tokens.append(f"PARAM_{key}")
        tokens.append(normalize_value(value))


def flatten_json(prefix: str, obj, tokens: list[str]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            key = clean_key(key)
            if not key:
                continue
            flatten_json(f"{prefix}_{key}", value, tokens)
    elif isinstance(obj, list):
        tokens.append(prefix)
        tokens.append("LIST")
    else:
        tokens.append(prefix)
        tokens.append(normalize_value(obj))


def add_body_tokens(tokens: list[str], body: str, headers: dict) -> None:
    body = (body or "").strip()
    if not body:
        return

    content_type = headers.get("Content-Type", "") or headers.get("content-type", "")
    content_type = content_type.lower()

    # 1) JSON body
    if "application/json" in content_type or body.startswith("{") or body.startswith("["):
        try:
            parsed = json.loads(body)
            flatten_json("BODY", parsed, tokens)
            return
        except Exception:
            pass

    # 2) Form-urlencoded body
    if "application/x-www-form-urlencoded" in content_type or "=" in body:
        try:
            pairs = parse_qsl(body, keep_blank_values=True)
            if pairs:
                for key, value in pairs:
                    key = clean_key(key)
                    if not key:
                        continue
                    tokens.append(f"BODY_{key}")
                    tokens.append(normalize_value(value))
                return
        except Exception:
            pass

    # 3) Fallback
    tokens.append("BODY_RAW")
    tokens.append(normalize_value(body))


def serialize_record(record: dict) -> str | None:
    method = (record.get("method") or "").upper()
    path = record.get("path") or ""
    query = record.get("query") or ""
    body = record.get("body") or ""
    headers = record.get("headers") or {}

    if not method or not path:
        return None

    if not should_keep(path):
        return None

    path = normalize_path(path)
    tokens = [f"METHOD_{method}", f"PATH_{path}"]

    if query:
        add_query_tokens(tokens, query)

    if body:
        add_body_tokens(tokens, body, headers)

    return " ".join(tokens)


def main():
    kept = 0
    skipped = 0
    raw_body_rows = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as fin, open(OUTPUT_FILE, "w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                skipped += 1
                continue

            serialized = serialize_record(record)
            if serialized is None:
                skipped += 1
                continue

            if "BODY_RAW" in serialized:
                raw_body_rows += 1

            fout.write(serialized + "\n")
            kept += 1

    print(f"Saved {kept} rows to {OUTPUT_FILE}")
    print(f"Skipped {skipped} rows")
    print(f"Rows still using BODY_RAW: {raw_body_rows}")


if __name__ == "__main__":
    main()