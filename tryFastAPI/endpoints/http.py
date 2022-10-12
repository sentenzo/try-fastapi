from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from tryFastAPI.db.connection.session import get_session_dependency as get_session
from tryFastAPI.db.models import Html
from tryFastAPI.crud import get_html, put_html, post_html

from tryFastAPI.schemas import HtmlInRequest, HtmlOutResponse

api_router = APIRouter(
    prefix="/http",
    tags=["Http"],
)


@api_router.get("/{key}/page", response_class=HTMLResponse)
async def get_http_as_page(key: str, db: Session = Depends(get_session)) -> str:
    html: Html = get_html(db, key=key)
    return html.html


@api_router.get("/{key}", response_model=HtmlOutResponse)
async def get_http(key: str, db: Session = Depends(get_session)):
    html: HtmlOutResponse = get_html(db, key=key)
    return html


@api_router.put("", response_model=HtmlOutResponse)
async def put_http(html_put: HtmlInRequest, db: Session = Depends(get_session)):
    db_html = get_html(db, key=html_put.key)
    if db_html:
        raise HTTPException(status_code=400, detail="Key already registered")
    return put_html(db, html_put)


@api_router.post("", response_model=HtmlOutResponse)
async def post_http(html_post: HtmlInRequest, db: Session = Depends(get_session)):
    db_html = get_html(db, key=html_post.key)
    if not db_html:
        raise HTTPException(status_code=400, detail="Key is not registered")
    return post_html(db, html_post)


@api_router.delete("/{key}", response_model=HtmlOutResponse)
async def delete_http(key: str, db: Session = Depends(get_session)):
    ...
