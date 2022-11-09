from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


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


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    id: UUID | None
