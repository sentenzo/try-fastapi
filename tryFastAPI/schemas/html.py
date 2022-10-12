from pydantic import BaseModel


class HtmlBase(BaseModel):
    key: str


class Html(BaseModel):
    key: str
    html: str

    class Config:
        orm_mode = True
