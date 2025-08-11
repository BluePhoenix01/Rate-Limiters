from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import time
from collections import deque

CAPACITY = 10   # Maximum tokens in the bucket
LEAK_RATE = 1   # Tokens to leak per second

app = FastAPI()
buckets: dict[str, deque[float]] = {}

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client is not None else "unknown"
    current_time = time.time()
    
    buckets[client_ip] = buckets.get(client_ip, deque(maxlen=CAPACITY))
    queue = buckets[client_ip]

    if queue and queue[0] < current_time - LEAK_RATE:
        queue.popleft()

    if len(queue) < CAPACITY:
        queue.append(current_time)
        return await call_next(request)
    else:
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

@app.get("/")
async def root():
    return {"message": "Hello World"}

