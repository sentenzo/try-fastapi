from uuid import UUID

from fastapi import HTTPException, status


class Exception404NoId(HTTPException):
    def __init__(
        self,
        entity_name: str,
        uuid: UUID,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No {entity_name} with id={uuid}",
        )


class Exception403(HTTPException):
    def __init__(
        self,
        detail: str,
    ) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
