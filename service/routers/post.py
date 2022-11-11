from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import func
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql.expression import or_

from .. import exceptions, models, oauth2, schemas
from ..database import get_db


router = APIRouter(prefix="/post", tags=["Post"])


class Exception404NoId(exceptions.Exception404NoId):
    def __init__(self, uuid: UUID) -> None:
        super().__init__("post", uuid)


def flatten_aggregation_funcs(
    row: tuple[models.Post, int]
) -> schemas.post.PostResponseVotes:
    post, votes_count = row
    sch_post = schemas.post.PostResponseWithOwner.from_orm(post)
    flat = sch_post.dict()
    flat["votes"] = votes_count
    return flat


@router.get(
    "/all",
    response_model=list[schemas.post.PostResponseVotes],
)
async def get_posts(
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
):
    posts_query = db.query(
        models.Post, func.count(models.Vote.user_id).label("votes")
    ).join(models.Vote, isouter=True)
    if search:
        posts_query = posts_query.filter(
            models.Post.title.ilike(f"%{search}%")
            | models.Post.content.ilike(f"%{search}%")
        )
    posts_query = (
        posts_query.group_by(models.Post.id)
        .order_by(models.Post.created_at)
        .limit(limit)
        .offset(offset)
    )

    print(posts_query)
    posts = posts_query.all()
    print(posts[0])

    return [flatten_aggregation_funcs(post) for post in posts]


@router.get(
    "/{post_uuid}",
    response_model=schemas.post.PostResponseVotes,
)
async def get_post(
    post_uuid: UUID,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    post_query = (
        db.query(models.Post, func.count(models.Vote.user_id).label("votes"))
        .join(models.Vote, isouter=True)
        .filter(models.Post.id == post_uuid)
        .group_by(models.Post.id)
    )
    post = post_query.first()
    if not post:
        raise Exception404NoId(post_uuid)
    return flatten_aggregation_funcs(post)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.post.PostResponse,
)
async def create_post(
    new_post: schemas.post.PostCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    new_post_args = new_post.dict()
    new_db_post = models.Post(owner_id=user.id, **new_post_args)
    db.add(new_db_post)
    db.commit()
    db.refresh(new_db_post)

    return new_db_post


@router.delete("/{post_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_uuid: UUID,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    to_be_deleted: models.Post = db.query(models.Post).get(post_uuid)

    if not to_be_deleted:
        raise Exception404NoId(post_uuid)
    if not to_be_deleted.owner_id == user.id:
        raise exceptions.Exception403(
            "It is only allowed to delete one's own posts"
        )
    db.delete(to_be_deleted)
    db.commit()


@router.put(
    "/{post_uuid}",
    response_model=schemas.post.PostResponse,
)
async def update_post(
    post_uuid: UUID,
    updated_post: schemas.post.PostCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    to_be_updated_query: Query = db.query(models.Post).filter(
        models.Post.id == post_uuid
    )
    to_be_updated = to_be_updated_query.first()

    if not to_be_updated:
        raise Exception404NoId(post_uuid)
    if not to_be_updated.owner_id == user.id:
        raise exceptions.Exception403(
            "It is only allowed to update one's own posts"
        )

    argvals = updated_post.dict()

    to_be_updated_query.update(argvals)
    db.commit()
    db.refresh(to_be_updated)

    return to_be_updated
