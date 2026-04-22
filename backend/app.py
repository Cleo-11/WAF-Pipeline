from flask import Flask, request, Response, jsonify
import requests
import os
import json
from datetime import datetime

from preprocess import serialize_request
from scanner import WAFScanner

app = Flask(__name__)

TARGET = "http://localhost:3000"
LOG_DIR = "../data"
RAW_LOG_FILE = os.path.join(LOG_DIR, "raw_requests.jsonl")
SCORE_LOG_FILE = os.path.join(LOG_DIR, "scored_requests.jsonl")

os.makedirs(LOG_DIR, exist_ok=True)

scanner = WAFScanner()


def log_raw_request(req):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": req.method,
        "path": req.path,
        "query": req.query_string.decode("utf-8", errors="ignore"),
        "headers": dict(req.headers),
        "body": req.get_data(as_text=True),
    }
    with open(RAW_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return record


def log_scored_request(raw_record, score_result):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": raw_record["method"],
        "path": raw_record["path"],
        "query": raw_record["query"],
        "serialized": score_result["serialized"],
        "route": score_result["route"],
        "mode": score_result["mode"],
        "score": score_result["score"],
        "threshold": score_result["threshold"],
        "verdict": score_result["verdict"],
    }
    with open(SCORE_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/scan", methods=["POST"])
def scan_only():
    payload = request.get_json(force=True)

    serialized = serialize_request(
        method=payload["method"],
        path=payload["path"],
        query=payload.get("query", ""),
        body=payload.get("body", ""),
        headers=payload.get("headers", {}),
    )

    if serialized is None:
        return jsonify({
            "scored": False,
            "reason": "filtered_static_or_ignored_route"
        })

    result = scanner.score_serialized(serialized)
    return jsonify(result)


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(path):
    raw_record = log_raw_request(request)

    serialized = serialize_request(
        method=request.method,
        path=request.path,
        query=request.query_string.decode("utf-8", errors="ignore"),
        body=request.get_data(as_text=True),
        headers=dict(request.headers),
    )

    if serialized is not None:
        score_result = scanner.score_serialized(serialized)
        log_scored_request(raw_record, score_result)

        if score_result["verdict"] == "SUSPICIOUS":
            print(
                f"[ALERT] {score_result['verdict']} "
                f"score={score_result['score']:.4f} "
                f"threshold={score_result['threshold']:.4f} "
                f"path={request.path}"
            )

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