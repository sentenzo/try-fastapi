# import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

# from sqlalchemy.orm import relationship
import sqlalchemy.dialects.postgresql as pg

from .db.database import Base


class Html(Base):
    __tablename__ = "tblHtml"

    # id = Column(pg.UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    key = Column(String, unique=True, index=True, primary_key=True)
    html = Column(pg.TEXT)
