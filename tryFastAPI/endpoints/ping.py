from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from tryFastAPI.schemas import SimpleResponce
from tryFastAPI.db.connection.session import get_session_dependency as get_session

api_router = APIRouter(
    prefix = "/ping",
    tags = ["Application Health"],
)


@api_router.get("/", response_model = SimpleResponce, status_code = status.HTTP_200_OK)
@api_router.get("/app", response_model = SimpleResponce, status_code = status.HTTP_200_OK)
async def ping_app():
    return SimpleResponce(message="Application responds")


@api_router.get("/db", response_model = SimpleResponce, status_code = status.HTTP_200_OK)
async def ping_db(db: Session = Depends(get_session)):
    result = await db.scalar(select(text("1")))
    if result:
        return SimpleResponce(message="Database responds")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database isn't working",
    )
