import dotenv
from fastapi import FastAPI
from passlib.context import CryptContext


# isort: off

dotenv.load_dotenv()
from .database import engine  # pylint: disable=wrong-import-position
from . import models  # pylint: disable=wrong-import-position

# isort: on

models.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()

__all__ = ["app", "pwd_context"]
