# KR2: Grigory
import os
import redis
from flask import Flask, request

app = Flask(__name__)
_redis = None

def get_redis():
    global _redis
    if _redis is None:
        _redis = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True,
        )
    return _redis

@app.route("/health")
def health():
    return "ok\n"

@app.route("/")
def index():
    r = get_redis()
    n = r.incr("hits")
    student = os.getenv("STUDENT", "unknown")
    cid = os.getenv("HOSTNAME", "local")[:12]
    return f"KR2 | {student} | container {cid} | hits: {n}\n"

@app.route("/whoami")
def whoami():
    scheme = request.headers.get("X-Forwarded-Proto", "none")
    client = request.headers.get("X-Real-IP", "none")
    host = request.headers.get("Host", "none")
    return f"scheme: {scheme}\nclient: {client}\nhost: {host}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
