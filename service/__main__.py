from random import randrange

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


class Post(BaseModel):
    id: int = Field(default_factory=lambda: randrange(1, 10**10))
    title: str
    content: str
    published: bool = True
    rating: int | None


class MockDb:
    def __init__(self) -> None:
        self.last_post_id = 0
        self.post: dict[Post] = {}

    def add_post(self, post: Post):
        self.last_post_id += 1
        self.post[post.id] = post


db = MockDb()


@app.get("/")
async def root():
    return {"message": "root"}


@app.get("/post")
async def get_posts():
    return {"data": db.post}


@app.post("/post")
async def create_post(new_post: Post):
    db.add_post(new_post)
    print(db.post)
    return new_post


if __name__ == "__main__":
    uvicorn.run("service.__main__:app", host="0.0.0.0", port=8000, reload=True)
