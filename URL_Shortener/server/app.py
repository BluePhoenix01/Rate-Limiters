from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from models import URL, get_db
from utils import encode_base62
import cache
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/shorten/")
async def shorten_url(request: Request, db=Depends(get_db)):
    data = await request.json()   
    url = data.get("url") 
    url = URL(original_url=url)

    db.add(url)
    db.commit()
    db.refresh(url)
    short_code = encode_base62(url.id)
    url.short_code = short_code
    db.commit()
    cache.set_cached_url(short_code, url.original_url)
    return {"short_url": f"http://localhost:8000/{short_code}"}

@app.get("/{short_code}")
def redirect_url(short_code: str, db=Depends(get_db)):
    url = cache.get_cached_url(short_code)
    if url:
        return RedirectResponse(url.decode())

    url = db.query(URL).filter(URL.short_code == short_code).first()
    if url:
        cache.set_cached_url(short_code, url.original_url)
        return RedirectResponse(url.original_url)

    raise HTTPException(status_code=404, detail="URL not found")



