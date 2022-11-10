from enum import IntEnum
from uuid import UUID

from pydantic import BaseModel


class VoteDirection(IntEnum):
    UP = 1
    DOWN = -1


class VoteCreate(BaseModel):
    post_id: UUID
    direction: VoteDirection
