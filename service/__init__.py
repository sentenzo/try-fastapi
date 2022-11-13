from passlib.context import CryptContext

from service.__main__ import app, make_app


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


__all__ = ["app", "make_app", "pwd_context"]
