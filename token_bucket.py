from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from redis import asyncio as aioredis
import time

MAX_TOKENS = 10          # Maximum tokens in the bucket
TOKENS_REFILL_RATE = 1   # Tokens to add per second

app = FastAPI()
redis = aioredis.from_url("redis://localhost:6379")

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client is not None else "unknown"
    token_bucket_key = f"token_bucket:{client_ip}"
    current_time = time.time()
    last_refill_key = f"{token_bucket_key}:last_refill"
    token_key = f"{token_bucket_key}:tokens"
    
    last_refill = float(await redis.get(last_refill_key) or current_time)
    tokens = float(await redis.get(token_key) or MAX_TOKENS)

    # Refill tokens based on the time elapsed since the last refill
    tokens = min(MAX_TOKENS, tokens + (current_time - last_refill) * TOKENS_REFILL_RATE)

    await redis.set(last_refill_key, current_time)
    
    if tokens >= 1:
        await redis.set(token_key, tokens - 1)
        return await call_next(request)
    else:
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

@app.get("/")
async def root():
    return {"message": "Hello World"}

