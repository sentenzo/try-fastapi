from datetime import datetime

from pydantic import BaseModel  # , Field


# from random import randrange


class PostBase(BaseModel):
    # id: int = Field(default_factory=lambda: randrange(1, 10**10))
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True
