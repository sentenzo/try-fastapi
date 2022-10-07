from time import sleep
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import sqlalchemy.exc as sql_exc

from . import crud, models, schemas
from .database import SessionLocal, engine


# for _ in range(20):  # 20*0.2 == 4 sec
#     try:
#         models.Base.metadata.create_all(bind=engine)
#         break
#     except sql_exc.OperationalError:
#         # when the app container launches up faster than db
#         print(" >>> so slow")
#         sleep(0.2)

#         continue


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
