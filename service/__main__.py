from random import randrange

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status

from pydantic import BaseModel, Field
from sqlalchemy.orm import Query, Session

from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


class Post(BaseModel):
    id: int = Field(default_factory=lambda: randrange(1, 10**10))
    title: str
    content: str
    published: bool = True


@app.get("/")
async def root():
    return {"message": "root"}


@app.get("/sqla")
def sqla(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/post/all")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/post/{post_id}")
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id={post_id}",
        )
    return post


@app.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(new_post: Post, db: Session = Depends(get_db)):
    new_post_args = new_post.dict()
    del new_post_args["id"]
    new_db_post = models.Post(**new_post_args)
    db.add(new_db_post)
    db.commit()
    db.refresh(new_db_post)

    return {"data": new_db_post}


@app.delete("/post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    to_be_deleted = db.query(models.Post).get(post_id)

    if not to_be_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id={post_id}",
        )
    db.delete(to_be_deleted)
    db.commit()


@app.put("/post/{post_id}")
async def update_post(
    post_id: int, updated_post: Post, db: Session = Depends(get_db)
):
    to_be_updated_query: Query = db.query(models.Post).filter(
        models.Post.id == post_id
    )
    to_be_updated = to_be_updated_query.first()

    if not to_be_updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id={post_id}",
        )

    argvals = updated_post.dict()
    del argvals["id"]

    to_be_updated_query.update(argvals)
    db.commit()
    db.refresh(to_be_updated)

    return {"data": to_be_updated}


if __name__ == "__main__":
    uvicorn.run("service.__main__:app", host="0.0.0.0", port=8000, reload=True)
