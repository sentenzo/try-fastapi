from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Query, Session

from .. import models, schemas
from ..database import get_db


router = APIRouter(prefix="/post", tags=["Post"])


@router.get(
    "/all",
    response_model=list[schemas.PostResponse],
)
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get(
    "/{post_uuid}",
    response_model=schemas.PostResponse,
)
async def get_post(post_uuid: UUID, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(post_uuid)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id={post_uuid}",
        )
    return post


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
)
async def create_post(
    new_post: schemas.PostCreate, db: Session = Depends(get_db)
):
    new_post_args = new_post.dict()
    new_db_post = models.Post(**new_post_args)
    db.add(new_db_post)
    db.commit()
    db.refresh(new_db_post)

    return new_db_post


@router.delete("/{post_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_uuid: UUID, db: Session = Depends(get_db)):
    to_be_deleted = db.query(models.Post).get(post_uuid)

    if not to_be_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id={post_uuid}",
        )
    db.delete(to_be_deleted)
    db.commit()


@router.put(
    "/{post_uuid}",
    response_model=schemas.PostResponse,
)
async def update_post(
    post_uuid: UUID,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
):
    to_be_updated_query: Query = db.query(models.Post).filter(
        models.Post.id == post_uuid
    )
    to_be_updated = to_be_updated_query.first()

    if not to_be_updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id={post_uuid}",
        )

    argvals = updated_post.dict()

    to_be_updated_query.update(argvals)
    db.commit()
    db.refresh(to_be_updated)

    return to_be_updated
