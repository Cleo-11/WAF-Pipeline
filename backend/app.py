from flask import Flask, request, Response
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

TARGET = "http://localhost:3000"
LOG_DIR = "../data"
LOG_FILE = os.path.join(LOG_DIR, "raw_requests.jsonl")

os.makedirs(LOG_DIR, exist_ok=True)


# --- FILTER RULES ---
IGNORE_PREFIXES = [
    "/assets/",
    "/media/",
    "/socket.io/",
]

IGNORE_SUFFIXES = [
    ".js", ".css", ".png", ".jpg", ".jpeg",
    ".gif", ".svg", ".ico", ".woff", ".woff2", ".ttf"
]

# Optional: only log meaningful routes
KEEP_PREFIXES = [
    "/rest/",
    "/api/",
    "/",  # keep homepage
]


def should_log(req):
    path = req.path

    # Ignore static prefixes
    for prefix in IGNORE_PREFIXES:
        if path.startswith(prefix):
            return False

    # Ignore static file extensions
    for suffix in IGNORE_SUFFIXES:
        if path.endswith(suffix):
            return False

    # Keep only meaningful routes
    if not any(path.startswith(p) for p in KEEP_PREFIXES):
        return False

    return True


def log_request(req):
    if not should_log(req):
        return

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": req.method,
        "path": req.path,
        "query": req.query_string.decode("utf-8", errors="ignore"),
        "headers": dict(req.headers),
        "body": req.get_data(as_text=True),
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(path):
    log_request(request)

    url = f"{TARGET}/{path}"

    resp = requests.request(
        method=request.method,
        url=url,
        headers={k: v for k, v in request.headers if k.lower() != "host"},
        params=request.args,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )

    excluded = {"content-encoding", "content-length", "transfer-encoding", "connection"}
    headers = [(k, v) for k, v in resp.raw.headers.items() if k.lower() not in excluded]

    return Response(resp.content, resp.status_code, headers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)