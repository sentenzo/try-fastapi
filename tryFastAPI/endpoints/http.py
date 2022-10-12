from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from tryFastAPI.db.connection.session import get_session_dependency as get_session
from tryFastAPI.db.models import Html
from tryFastAPI.crud.html import get_html, put_html, post_html, delete_html

from tryFastAPI.schemas import Html as HtmlSchema
from tryFastAPI.schemas import SimpleResponce

api_router = APIRouter(
    prefix="/http",
    tags=["Http"],
)


@api_router.get("/{key}/page", response_class=HTMLResponse)
async def get_http_as_page(key: str, db: Session = Depends(get_session)) -> str:
    html: Html = get_html(db, key=key)
    return html.html


@api_router.get("/{key}", response_model=HtmlSchema)
async def get_http(key: str, db: Session = Depends(get_session)):
    response = get_html(db, key=key)
    if not response:
        raise HTTPException(status_code=404, detail="No such key")
    return response


@api_router.put("", response_model=HtmlSchema)
async def put_http(html_put: HtmlSchema, db: Session = Depends(get_session)):
    response = put_html(db, html_put)
    if not response:
        raise HTTPException(status_code=409, detail="Key already registered")
    return response


@api_router.post("", response_model=HtmlSchema)
async def post_http(html_post: HtmlSchema, db: Session = Depends(get_session)):
    response = post_html(db, html_post)
    if not response:
        raise HTTPException(status_code=404, detail="No such key")
    return response


@api_router.delete("/{key}", response_model=SimpleResponce)
async def delete_http(key: str, db: Session = Depends(get_session)):
    response = delete_html(db, key)
    if not response:
        raise HTTPException(status_code=404, detail="No such key")
    return SimpleResponce(message="Successfully deleted")
