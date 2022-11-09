from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, oauth2, pwd_context, schemas
from ..database import get_db


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=schemas.misc.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    db_user: models.User | None = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if not db_user or not pwd_context.verify(
        user_credentials.password, db_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    user_id: UUID = db_user.id
    token = oauth2.create_access_token(data={"user_id": str(user_id)})
    return {"token": token, "token_type": "bearer"}
