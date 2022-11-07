from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Post(Base):
    """
    CREATE TABLE IF NOT EXISTS public.post
    (
        id integer NOT NULL DEFAULT nextval('post_id_seq'::regclass),
        created_at timestamp with time zone NOT NULL DEFAULT now(),
        title character varying COLLATE pg_catalog."default" NOT NULL,
        content character varying COLLATE pg_catalog."default" NOT NULL,
        published boolean NOT NULL DEFAULT true,
        CONSTRAINT post_pkey PRIMARY KEY (id)
    )
    """

    __tablename__ = "post"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(
        Boolean, nullable=False, default=True, server_default="TRUE"
    )
