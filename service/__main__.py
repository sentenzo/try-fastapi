from random import randrange

import uvicorn
from fastapi import FastAPI, Response, status, HTTPException
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


@app.get("/post/all")
async def get_posts():
    return {"data": db.post}


@app.get("/post/{id}")
async def get_post(id: int, responce: Response):
    if not id in db.post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id={id}")
    else:
        return {"data": db.post[id]}


@app.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    db.add_post(new_post)
    print(db.post)
    return new_post


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    if not id in db.post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id={id}")
    else:
        del db.post[id]


@app.put("/post/{id}")
async def update_post(id: int, updated_post: Post):
    if not id in db.post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id={id}")
    else:
        db.post[id] = updated_post
        db.post[id].id = id
        return {"data": db.post[id]}


if __name__ == "__main__":
    uvicorn.run("service.__main__:app", host="0.0.0.0", port=8000, reload=True)
