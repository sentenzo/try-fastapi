from sqlalchemy.orm import Session

from tryFastAPI.db.models import Html

from tryFastAPI.schemas import HtmlInRequest, HtmlOutResponse


def get_html(session: Session, key: str) -> HtmlOutResponse:
    html = session.query(Html).filter(Html.key == key).first()
    return HtmlOutResponse(key=html.key, html=html.html)


def put_html(session: Session, html: HtmlInRequest):
    db_html = Html(key=html.key, html=html.html)
    session.add(db_html)
    session.commit()
    session.refresh(db_html)
    return db_html


def post_html(session: Session, html: HtmlInRequest):
    db_html = get_html(session, html.key)
    db_html.html = html.html
    session.commit()
    session.refresh(db_html)
    return db_html


def delete_html(session: Session, key: str):
    ...
