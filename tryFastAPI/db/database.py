from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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
ldub: DbUrlEnvBuilder = DbUriBuilderLocal()
SQL_DATABASE_URL = ldub.from_env().to_str()

engine = create_engine(SQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
