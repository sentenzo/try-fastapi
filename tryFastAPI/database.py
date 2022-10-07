from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .db.db_url_builder import (
    db_url_env_builder_factory,
    DbUrlEnvBuilder,
    DbUrlParams,
)

env_mapping = {
    DbUrlParams.PROTOCOL: "DB_PROTOCOL",
    DbUrlParams.USER: "DB_USER",
    DbUrlParams.PASSWPRD: "DB_PASSWORD",
    DbUrlParams.HOST: "DB_HOST",
    DbUrlParams.PORT: "DB_PORT",
    DbUrlParams.DBNAME: "DB_DBNAME",
}

LocalDbUriBuilder = db_url_env_builder_factory(env_mapping=env_mapping)
ldub: DbUrlEnvBuilder = LocalDbUriBuilder()
SQLALCHEMY_DATABASE_URL = ldub.from_env().to_str()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
