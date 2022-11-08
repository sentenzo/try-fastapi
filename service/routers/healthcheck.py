from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select, text

from ..database import get_db


router = APIRouter(prefix="/healthcheck", tags=["Healthcheck"])


@router.get("/ping_app", status_code=status.HTTP_200_OK)
def ping_app():
    return {"message": "the application is running"}


@router.get("/ping_db", status_code=status.HTTP_200_OK)
def ping_db(db: Session = Depends(get_db)):
    db.scalar(select(text("NOW()")))
    return {"message": "the db is reachable"}
