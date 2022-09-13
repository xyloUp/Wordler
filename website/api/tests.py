from httpx import get, post

BASE = "http://127.0.0.1:5000"

def try_get():
    req = get(f"{BASE}/words")
    print(req.json())

def try_post():
    req = post(f"{BASE}/auth/login", json={"username": "tla", "password": "whipnana"})
    print(req.json(), req.status_code)

try_post()