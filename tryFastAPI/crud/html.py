from sqlalchemy.ext.asyncio import AsyncSession

from tryFastAPI.db.models import Html
from tryFastAPI.schemas import Html as HtmlSchema


async def get_html(session: AsyncSession, key: str) -> HtmlSchema | None:
    html = await session.get(Html, key)
    return HtmlSchema.from_orm(html) if html else None


async def put_html(session: AsyncSession, html: HtmlSchema) -> HtmlSchema | None:
    if await session.get(Html, html.key):
        return None
    db_html = Html(key=html.key, html=html.html)
    session.add(db_html)
    await session.commit()
    await session.refresh(db_html)
    return HtmlSchema.from_orm(db_html)


async def post_html(session: AsyncSession, html: HtmlSchema):
    db_html = await session.get(Html, html.key)
    if not db_html:
        return None
    db_html.html = html.html
    await session.commit()
    await session.refresh(db_html)
    return db_html


async def delete_html(session: AsyncSession, key: str):
    db_html = await session.get(Html, key)
    if not db_html:
        return False
    await session.delete(db_html)
    await session.commit()
    return True
