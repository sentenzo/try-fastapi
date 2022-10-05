from sqlalchemy.orm import Session

from . import models, schemas


def get_html(db: Session, key: str):
    return db.query(models.Html).filter(models.Html.key == key).first()


def put_html(db: Session, html: schemas.Html):
    db_html = models.Html(key=html.key, html=html.html)
    db.add(db_html)
    db.commit()
    db.refresh(db_html)
    return db_html
