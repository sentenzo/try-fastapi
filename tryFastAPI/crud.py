from sqlalchemy.orm import Session

from .db.models import Html as mHtml

from .schemas import Html as sHtml


def get_html(db: Session, key: str):
    return db.query(mHtml).filter(mHtml.key == key).first()


def put_html(db: Session, html: sHtml):
    db_html = mHtml(key=html.key, html=html.html)
    db.add(db_html)
    db.commit()
    db.refresh(db_html)
    return db_html
