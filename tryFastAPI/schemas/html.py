from pydantic import BaseModel


class HtmlBase(BaseModel):
    key: str

class HtmlGetRequest(HtmlBase):
    class Config:
        orm_mode = True

class HtmlInRequest(HtmlBase):
    html: str

    class Config:
        orm_mode = True


class HtmlOutResponse(HtmlBase):
    html: str

    class Config:
        orm_mode = True
