from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text


async def test_select_1(acync_session: AsyncSession):
    result = await acync_session.scalar(select(text("1")))
    assert result == 1
