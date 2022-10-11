from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    Query,
    Request,
    Response,
)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session


api_router = APIRouter(
    prefix="/http",
    tags=["Http"],
)


# @api_router.get("/{key}", response_class=HTMLResponse)
# async def get_http(key: str, db: Session = Depends(get_db)) -> str:
#     html = crud.get_html(db, key=key)
#     return html.html
