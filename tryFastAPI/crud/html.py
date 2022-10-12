from sqlalchemy.orm import Session

from tryFastAPI.db.models import Html

from tryFastAPI.schemas import Html as HtmlSchema


def get_html(session: Session, key: str) -> HtmlSchema | None:
    html = session.query(Html).get(key)
    return HtmlSchema.from_orm(html) if html else None


def put_html(session: Session, html: HtmlSchema) -> HtmlSchema | None:
    if session.query(Html).get(html.key):
        return None
    db_html = Html(key=html.key, html=html.html)
    session.add(db_html)
    session.commit()
    session.refresh(db_html)
    return HtmlSchema.from_orm(db_html)


def post_html(session: Session, html: HtmlSchema):
    db_html = session.query(Html).get(html.key)
    if not db_html:
        return None
    db_html.html = html.html
    session.commit()
    session.refresh(db_html)
    return db_html


def delete_html(session: Session, key: str):
    db_html = session.query(Html).get(key)
    if not db_html:
        return False
    session.delete(db_html)
    session.commit()
    return True
