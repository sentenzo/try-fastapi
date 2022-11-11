from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from . import user


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostWithID(BaseModel):
    id: UUID
    created_at: datetime
    owner_id: UUID


class PostCreate(Post):
    pass


class PostResponse(Post, PostWithID):
    class Config:
        orm_mode = True


class PostResponseWithOwner(PostResponse):
    owner: user.UserResponse

    class Config:
        orm_mode = True


class PostResponseVotes(PostResponseWithOwner):
    votes: int
