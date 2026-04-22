import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, Any, Optional

import requests

BASE_URL = "http://192.168.1.6:5000"
TOTAL_REQUESTS = 10000
MAX_WORKERS = 20
REQUEST_TIMEOUT = 5
SLEEP_BETWEEN_REQUESTS = 0.02

SEARCH_TERMS = [
    "",
    "apple",
    "banana",
    "juice",
    "smoothie",
    "lemon",
    "mug",
    "sticker",
    "hoodie",
    "delivery",
]

WHOAMI_FIELDS = [
    None,
    "email",
]

PRODUCT_IDS = [1, 6, 8, 10, 12, 15, 20, 24, 25, 33, 42]

ROUTE_TYPES = [
    "home",
    "app_version",
    "app_config",
    "score_board",
    "whoami",
    "languages",
    "quantitys",
    "search",
    "product_detail",
    "reviews",
    "bootstrap_flow",
]

ROUTE_WEIGHTS = [
    8,   # home
    3,   # app_version
    4,   # app_config
    8,   # score_board
    14,  # whoami
    10,  # languages
    12,  # quantitys
    22,  # search
    10,  # product_detail
    5,   # reviews
    8,   # bootstrap_flow
]


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/147.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "application/json, text/plain, */*",
        }
    )
    return session


def make_get(
    session: requests.Session,
    path: str,
    params: Optional[Dict[str, Any]] = None,
) -> int:
    url = f"{BASE_URL}{path}"
    resp = session.get(url, params=params, timeout=REQUEST_TIMEOUT)
    return resp.status_code


def benign_get_request(session: requests.Session) -> tuple[int, str]:
    route_type = random.choices(ROUTE_TYPES, weights=ROUTE_WEIGHTS, k=1)[0]

    if route_type == "home":
        return make_get(session, "/"), route_type

    if route_type == "app_version":
        return make_get(session, "/rest/admin/application-version"), route_type

    if route_type == "app_config":
        return make_get(session, "/rest/admin/application-configuration"), route_type

    if route_type == "score_board":
        return make_get(
            session,
            "/api/Challenges/",
            {"name": "Score Board"},
        ), route_type

    if route_type == "whoami":
        field = random.choice(WHOAMI_FIELDS)
        if field is None:
            return make_get(session, "/rest/user/whoami"), route_type
        return make_get(session, "/rest/user/whoami", {"fields": field}), route_type

    if route_type == "languages":
        return make_get(session, "/rest/languages"), route_type

    if route_type == "quantitys":
        return make_get(session, "/api/Quantitys/"), route_type

    if route_type == "search":
        term = random.choice(SEARCH_TERMS)
        return make_get(session, "/rest/products/search", {"q": term}), route_type

    if route_type == "product_detail":
        product_id = random.choice(PRODUCT_IDS)
        return make_get(
            session,
            f"/api/Products/{product_id}",
            {"d": datetime.now().strftime("%a %b %d %Y")},
        ), route_type

    if route_type == "reviews":
        product_id = random.choice(PRODUCT_IDS)
        return make_get(session, f"/rest/products/{product_id}/reviews"), route_type

    if route_type == "bootstrap_flow":
        make_get(session, "/")
        make_get(session, "/rest/admin/application-version")
        make_get(session, "/rest/admin/application-configuration")
        make_get(session, "/api/Challenges/", {"name": "Score Board"})
        make_get(session, "/rest/languages")
        make_get(session, "/api/Quantitys/")
        make_get(session, "/rest/user/whoami", {"fields": "email"})
        status = make_get(session, "/rest/products/search", {"q": random.choice(SEARCH_TERMS)})
        return status, route_type

    return make_get(session, "/"), "fallback"


def worker(num_requests: int, worker_id: int) -> Dict[str, Any]:
    session = build_session()

    stats = {
        "worker_id": worker_id,
        "sent": 0,
        "success_2xx": 0,
        "redirect_3xx": 0,
        "client_4xx": 0,
        "server_5xx": 0,
        "exceptions": 0,
        "by_route": {},
    }

    for _ in range(num_requests):
        try:
            status, route_type = benign_get_request(session)
            stats["sent"] += 1
            stats["by_route"][route_type] = stats["by_route"].get(route_type, 0) + 1

            if 200 <= status < 300:
                stats["success_2xx"] += 1
            elif 300 <= status < 400:
                stats["redirect_3xx"] += 1
            elif 400 <= status < 500:
                stats["client_4xx"] += 1
            elif 500 <= status < 600:
                stats["server_5xx"] += 1

            time.sleep(SLEEP_BETWEEN_REQUESTS)

        except Exception:
            stats["sent"] += 1
            stats["exceptions"] += 1

    return stats


def chunk_requests(total: int, workers: int):
    base = total // workers
    remainder = total % workers
    chunks = [base] * workers
    for i in range(remainder):
        chunks[i] += 1
    return chunks


def main():
    print("Starting benign GET traffic generation")
    print(f"Base URL       : {BASE_URL}")
    print(f"Total requests : {TOTAL_REQUESTS}")
    print(f"Max workers    : {MAX_WORKERS}")

    chunks = chunk_requests(TOTAL_REQUESTS, MAX_WORKERS)

    aggregate = {
        "sent": 0,
        "success_2xx": 0,
        "redirect_3xx": 0,
        "client_4xx": 0,
        "server_5xx": 0,
        "exceptions": 0,
    }

    route_totals: Dict[str, int] = {}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(worker, count, idx)
            for idx, count in enumerate(chunks, start=1)
            if count > 0
        ]

        for future in as_completed(futures):
            stats = future.result()

            aggregate["sent"] += stats["sent"]
            aggregate["success_2xx"] += stats["success_2xx"]
            aggregate["redirect_3xx"] += stats["redirect_3xx"]
            aggregate["client_4xx"] += stats["client_4xx"]
            aggregate["server_5xx"] += stats["server_5xx"]
            aggregate["exceptions"] += stats["exceptions"]

            for route, count in stats["by_route"].items():
                route_totals[route] = route_totals.get(route, 0) + count

            print(
                f"Worker {stats['worker_id']:02d} | "
                f"sent={stats['sent']} "
                f"2xx={stats['success_2xx']} "
                f"3xx={stats['redirect_3xx']} "
                f"4xx={stats['client_4xx']} "
                f"5xx={stats['server_5xx']} "
                f"exc={stats['exceptions']}"
            )

    print("-" * 60)
    print("Finished")
    print(f"Total sent   : {aggregate['sent']}")
    print(f"2xx success  : {aggregate['success_2xx']}")
    print(f"3xx redirect : {aggregate['redirect_3xx']}")
    print(f"4xx client   : {aggregate['client_4xx']}")
    print(f"5xx server   : {aggregate['server_5xx']}")
    print(f"Exceptions   : {aggregate['exceptions']}")
    print("-" * 60)
    print("Route distribution:")
    for route, count in sorted(route_totals.items(), key=lambda x: (-x[1], x[0])):
        print(f"{route:16s} {count}")


if __name__ == "__main__":
    main()