import requests
import random
import time

BASE = "http://192.168.1.6:5000"

paths = [
    "/",
    "/#/login",
    "/#/search",
    "/#/contact",
    "/#/score-board",
    "/rest/products/search?q=apple",
    "/rest/products/search?q=laptop",
    "/rest/products/search?q=phone",
    "/api/Challenges",
    "/api/Products",
]

for i in range(5000):
    path = random.choice(paths)
    try:
        requests.get(BASE + path, timeout=3)
    except Exception:
        pass

    if i % 500 == 0:
        print("sent", i)

    time.sleep(0.02)