from pydantic import BaseModel


class PingResponce(BaseModel):
    message: str
