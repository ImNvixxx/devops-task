from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
import psycopg2
import os
from prometheus_client import Counter, generate_latest

app = FastAPI()


REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests"
)


DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def db_connected():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        conn.close()
        return True

    except Exception:
        return False


@app.get("/")
def home():
    REQUEST_COUNT.inc()

    return {
        "message": "Hello DevOps Task"
    }


@app.get("/live")
def live():

    return {
        "status": "alive"
    }


@app.get("/health/ready")
def ready():

    if db_connected():

        return {
            "status": "ready"
        }

    raise HTTPException(
        status_code=503,
        detail="Database not ready"
    )


@app.get("/health")
def health():

    if db_connected():

        return {
            "status": "healthy",
            "database": "connected"
        }


    return {
        "status": "unhealthy",
        "database": "down"
    }


@app.get("/metrics")
def metrics():

    return PlainTextResponse(
        generate_latest().decode()
    )
@app.post("/alerts")
async def receive_alert(request: Request):

    payload = await request.json()

    print("=== ALERT RECEIVED ===")
    print(payload)

    return {
        "status": "received"
    }
