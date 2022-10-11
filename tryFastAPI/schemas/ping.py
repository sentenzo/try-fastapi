from pydantic import BaseModel


class PingBase(BaseModel):
    message: str


class PingApp(PingBase):
    pass


class PingDb(PingBase):
    pass
