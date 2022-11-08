import os
from datetime import datetime, timedelta
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

SECRET_KEY = os.environ.get("JWK")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365


def create_access_token(data: dict):
    data_to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"expire": expire.isoformat()})

    token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token: str, credentials_exception):
    try:
        data = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id: UUID | None = data.get("user_id", None)
        if not user_id:
            raise credentials_exception
        expire: datetime = datetime.fromisoformat(data.get("expire"))
        if expire < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The token is expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = schemas.TokenData(id=user_id)
        return token_data
    except JWTError as err:
        raise credentials_exception from err


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Failed to validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)
