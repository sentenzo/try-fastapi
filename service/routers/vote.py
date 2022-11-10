from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db


router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def vote(
    new_vote: schemas.vote.VoteCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).get(new_vote.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist",
        )
    db_vote = (
        db.query(models.Vote)
        .filter(
            models.Vote.post_id == new_vote.post_id,
            models.Vote.user_id == user.id,
        )
        .first()
    )
    if new_vote.direction == 1:

        if db_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The vote (uid={user.id}, pid={new_vote.post_id}) already exists",
            )
        else:
            new_db_vote = models.Vote(user_id=user.id, post_id=new_vote.post_id)
            db.add(new_db_vote)
            db.commit()
            db_vote = new_db_vote
        return {"message": "successfully voted"}
    else:
        if db_vote:
            db.delete(db_vote)
            db.commit()
            return PlainTextResponse(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote does not exist",
            )
    return
