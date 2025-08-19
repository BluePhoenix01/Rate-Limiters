import redis

cache = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_url(short_code):
    return cache.get(short_code)

def set_cached_url(short_code, original_url):
    cache.set(short_code, original_url)
