from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine


from .db_url_builder import DbUrlEnvBuilder, DbUrlParams

env_mapping = {
    DbUrlParams.PROTOCOL: "DB_PROTOCOL",
    DbUrlParams.USER: "DB_USER",
    DbUrlParams.PASSWPRD: "DB_PASSWORD",
    DbUrlParams.HOST: "DB_HOST",
    DbUrlParams.PORT: "DB_PORT",
    DbUrlParams.DBNAME: "DB_DBNAME",
}
DbUriBuilderLocal = DbUrlEnvBuilder.get_local_type(env_mapping)


def make_engine() -> Engine:
    sql_db_url = DbUriBuilderLocal().from_env().to_str()
    engine = create_engine(sql_db_url)
    return engine


def make_session_local_type(engine: Engine = None):
    engine = engine or make_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


#########

Base = declarative_base()

# SQL_DATABASE_URL = DbUriBuilderLocal().from_env().to_str()

# engine = make_engine()
# SessionLocal = make_session_local_type(engine)
