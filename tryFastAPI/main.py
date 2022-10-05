from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.put("/set/http", response_model=schemas.Html)
async def set_http(html: schemas.Html, db: Session = Depends(get_db)) -> None:
    db_html = crud.get_html(db, key=html.key)
    if db_html:
        raise HTTPException(status_code=400, detail="Key already registered")

    return crud.put_html(db=db, html=html)


@app.get("/get/http/{key}", response_class=HTMLResponse)
async def get_http(key: str, db: Session = Depends(get_db)) -> str:
    html = crud.get_html(db, key=key)
    return html.html
