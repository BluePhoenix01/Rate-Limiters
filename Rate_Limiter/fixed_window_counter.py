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
    time_frame = int(time.time())//WINDOW_SIZE

    key = f"rate_limit:{client_ip}:{time_frame}"
    current_reqs = await redis.incr(key)
    if current_reqs == 1:
        await redis.expire(key, WINDOW_SIZE)

    if current_reqs > RATE_LIMIT:
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
    else:
        return await call_next(request)

@app.get("/")
async def root():
    return {"message": "Hello World"}

