from pydantic import BaseModel


class SimpleResponce(BaseModel):
    message: str
