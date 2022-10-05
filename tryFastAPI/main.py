from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


HTTP_STORAGE = {}


@app.put("/set/http")
async def set_http(key: str, http: str) -> None:
    HTTP_STORAGE[key] = http


@app.get("/get/http/{key}", response_class=HTMLResponse)
async def get_http(key: str) -> str:
    html = f"<p>Key not found: {key}</p>"
    return HTTP_STORAGE.get(key, html)
