import json
import re
from urllib.parse import parse_qsl, unquote_plus


DROP_PREFIXES = [
    "/rest/admin",
    "/assets",
    "/media",
    "/socket.io",
]

DROP_SUFFIXES = [
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif",
    ".svg", ".woff", ".woff2", ".ico", ".map",
]


def should_score(path: str) -> bool:
    if not path:
        return False

    for prefix in DROP_PREFIXES:
        if path.startswith(prefix):
            return False

    for suffix in DROP_SUFFIXES:
        if path.endswith(suffix):
            return False

    return True


def normalize_path(path: str) -> str:
    path = re.sub(r"/\d+(/|$)", r"/NUM\1", path)
    path = re.sub(r"/+", "/", path)
    return path


def normalize_value(value) -> str:
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

    if "application/json" in content_type or body.startswith("{") or body.startswith("["):
        try:
            parsed = json.loads(body)
            flatten_json("BODY", parsed, tokens)
            return
        except Exception:
            pass

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

    tokens.append("BODY_RAW")
    tokens.append(normalize_value(body))


def suspicious_markers(raw: str) -> list[str]:
    decoded = unquote_plus(raw or "")
    raw_lower = decoded.lower()
    markers = []

    if " or " in raw_lower:
        markers.append("RAWTOKEN_or")
    if "union" in raw_lower:
        markers.append("RAWTOKEN_union")
    if "select" in raw_lower:
        markers.append("RAWTOKEN_select")
    if "sleep(" in raw_lower:
        markers.append("RAWTOKEN_sleep")
    if "<script" in raw_lower:
        markers.append("RAWTOKEN_script")
    if "onerror" in raw_lower:
        markers.append("RAWTOKEN_onerror")
    if "onload" in raw_lower:
        markers.append("RAWTOKEN_onload")
    if "../" in raw_lower:
        markers.append("RAWTOKEN_traversal")

    return markers


def serialize_request(method: str, path: str, query: str, body: str, headers: dict) -> str | None:
    if not should_score(path):
        return None

    path = normalize_path(path)
    tokens = [f"METHOD_{method.upper()}", f"PATH_{path}"]

    if query:
        add_query_tokens(tokens, query)

    if body:
        add_body_tokens(tokens, body, headers)

    raw_combined = " ".join([query or "", body or ""])
    tokens.extend(suspicious_markers(raw_combined))

    return " ".join(tokens)


def extract_route_key(serialized_request: str) -> str:
    for token in serialized_request.split():
        if token.startswith("PATH_"):
            return token
    return "UNKNOWN_ROUTE"


def map_route_group(route: str) -> str:
    if route.startswith("PATH_/rest/user") or route.startswith("PATH_/api/Users"):
        return "USER"
    if route.startswith("PATH_/rest/products") or route.startswith("PATH_/api/Products"):
        return "PRODUCT"
    if route.startswith("PATH_/rest/basket") or route.startswith("PATH_/api/BasketItems"):
        return "BASKET"
    if route.startswith("PATH_/api/Quantitys") or route.startswith("PATH_/rest/languages"):
        return "META"
    return "OTHER"