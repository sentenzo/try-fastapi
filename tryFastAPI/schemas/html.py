from pydantic import BaseModel


class HtmlBase(BaseModel):
    pass


class Html(HtmlBase):
    key: str
    html: str

    class Config:
        orm_mode = True