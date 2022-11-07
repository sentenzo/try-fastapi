# import time
from random import randrange

# import psycopg2
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status

# from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, Field
from sqlalchemy.orm import Query, Session

from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# while True:
#     try:
#         conn = psycopg2.connect(
#             host="---",
#             database="---",
#             user="---",
#             password="---",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         break
#     except Exception as error:
#         print("Exception:", error)
#         time.sleep(2)

# class MockDb:
#     def __init__(self) -> None:
#         self.last_post_id = 0
#         self.post: dict[Post] = {}

#     def add_post(self, post: Post):
#         self.last_post_id += 1
#         self.post[post.id] = post


# db = MockDb()


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
    # posts = db.query(models.Post).all()
    # cursor.execute("SELECT * FROM post")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/post/{post_id}")
async def get_post(post_id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM post WHERE id = %s", (post_id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).get(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id={post_id}",
        )
    return post


@app.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(new_post: Post, db: Session = Depends(get_db)):
    #     cursor.execute(
    #         """
    # INSERT INTO post (title, content, published)
    # VALUES (%s, %s, %s)
    # RETURNING *
    #     """,
    #         (new_post.title, new_post.content, new_post.published),
    #     )
    #     new_db_post = cursor.fetchone()
    #     conn.commit()
    new_post_args = new_post.dict()
    del new_post_args["id"]
    new_db_post = models.Post(**new_post_args)
    db.add(new_db_post)
    db.commit()
    db.refresh(new_db_post)

    return {"data": new_db_post}


@app.delete("/post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    # cursor.execute("DELETE FROM post WHERE id = %s RETURNING *", (post_id,))
    # deleted = cursor.fetchall()
    # db.delete(to_be_deleted)
    # conn.commit()
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
    #     cursor.execute(
    #         """
    # UPDATE post SET title=%s, content=%s, published=%s
    # WHERE id = %s
    # RETURNING *
    #     """,
    #         (
    #             updated_post.title,
    #             updated_post.content,
    #             updated_post.published,
    #             post_id,
    #         ),
    #     )
    #     updated = cursor.fetchone()
    # conn.commit()

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
