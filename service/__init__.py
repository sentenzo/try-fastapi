import dotenv
from fastapi import FastAPI
from passlib.context import CryptContext

from . import models
from .database import engine


dotenv.load_dotenv()
models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI()

__all__ = ["app", "pwd_context"]
