from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, pwd_context, schemas
from ..database import get_db


router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponse,
)
def create_user(
    new_user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    new_user.password = pwd_context.hash(new_user.password)
    new_db_user = models.User(**new_user.dict())
    db.add(new_db_user)
    try:
        db.commit()
    except IntegrityError as err:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        ) from err
    db.refresh(new_db_user)
    return new_db_user


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.UserResponse],
)
def get_all_users(
    db: Session = Depends(get_db),
):
    return db.query(models.User).all()


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserResponse,
)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with id={user_id}",
        )
    return user
