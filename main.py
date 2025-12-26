from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import string
import random

app = FastAPI(title="")


url_store = {}
visit_count = {}

BASE_URL = "http://localhost:8000"

class URLRequest(BaseModel):
    long_url: HttpUrl

class URLResponse(BaseModel):
    short_url: str


def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


@app.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest):
    short_code = generate_short_code()

    while short_code in url_store:
        short_code = generate_short_code()

    url_store[short_code] = request.long_url
    visit_count[short_code] = 0

    return {"short_url": f"{BASE_URL}/{short_code}"}


@app.get("/{short_code}")
def redirect_url(short_code: str):
    if short_code not in url_store:
        raise HTTPException(status_code=404, detail="URL not found")

    visit_count[short_code] += 1
    return RedirectResponse(url_store[short_code])


@app.get("/stats/{short_code}")
def get_stats(short_code: str):
    if short_code not in url_store:
        raise HTTPException(status_code=404, detail="URL not found")

    return {
        "original_url": url_store[short_code],
        "visit_count": visit_count[short_code]
    }