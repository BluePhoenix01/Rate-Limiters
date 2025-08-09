from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from redis import asyncio as aioredis
import time

RATE_LIMIT = 10         # Maximum requests per window
WINDOW_SIZE =  60       # Size of each window in seconds

app = FastAPI()
redis = aioredis.from_url("redis://localhost:6379")

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client is not None else "unknown"
    key_current = f"rate_limit:{client_ip}:{int(time.time() // WINDOW_SIZE)}"
    key_prev = f"rate_limit:{client_ip}:{int(time.time() // WINDOW_SIZE) - 1}"

    now = int(time.time())
    current_window_start = now // WINDOW_SIZE * WINDOW_SIZE
    elapsed_ratio = (now - current_window_start) / WINDOW_SIZE

    # Increment count for current window
    current_count = await redis.incr(key_current)
    if current_count == 1:
        await redis.expire(key_current, WINDOW_SIZE * 2)  # keep for overlap calc

    # Get previous window count (may be None)
    prev_count = await redis.get(key_prev)
    prev_count = int(prev_count) if prev_count else 0

    # Sliding window weighted sum
    weighted_count = prev_count * (1 - elapsed_ratio) + current_count

    if weighted_count > RATE_LIMIT:
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

    return await call_next(request)

@app.get("/")
async def root():
    return {"message": "Hello World"}

