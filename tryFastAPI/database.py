import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
user = os.environ["POSTGRES_USER"]
passwd = os.environ["POSTGRES_PASSWORD"]
dbname = os.environ["POSTGRES_DB"]
dbport = os.environ["POSTGRES_PORT"]
host = "localhost"

if os.path.isfile("/.dockerenv"):
    host = os.environ["PROJ_LOWER_NAME"] + "_postgres"
    dbport = 5432

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{passwd}@{host}:{dbport}/{dbname}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  # connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
