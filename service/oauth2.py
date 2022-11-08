import os
from datetime import datetime, timedelta

from jose import JWTError, jwt


SECRET_KEY = os.environ.get("JWK")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    data_to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"expire": expire.isoformat()})

    token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token
