from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2 import Error as Psycopg2Error
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select, text

from ..database import get_db


router = APIRouter(prefix="/healthcheck", tags=["Healthcheck"])


@router.get("/ping_app", status_code=status.HTTP_200_OK)
def ping_app():
    return {"message": "the application is running"}


@router.get("/ping_db", status_code=status.HTTP_200_OK)
def ping_db(db: Session = Depends(get_db)):
    try:
        db.scalar(select(text("NOW()")))  # SELECT NOW()
        return {"message": "the db is reachable"}
    except (Psycopg2Error, SQLAlchemyError) as ex:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to connect to database",
        ) from ex
