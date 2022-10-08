import os
from uuid import uuid4

import pytest
import dotenv
from sqlalchemy_utils import create_database, database_exists, drop_database
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig

from tryFastAPI.db.database import DbUriBuilderLocal

dotenv.load_dotenv()


@pytest.fixture
def db() -> str:
    prev_db_name = os.environ["DB_DBNAME"]
    tmp_db_url = None
    try:
        tmp_db_name = f"{prev_db_name}-pytest-{uuid4().hex}"
        os.environ["DB_DBNAME"] = tmp_db_name
        tmp_db_url = DbUriBuilderLocal().from_env().to_str()
        if not database_exists(tmp_db_url):
            create_database(tmp_db_url)
            yield tmp_db_url
    finally:
        os.environ["DB_DBNAME"] = prev_db_name
        if tmp_db_url and database_exists(tmp_db_url):
            drop_database(tmp_db_url)


@pytest.fixture
def migrated_db(db):
    alembic_config = AlembicConfig(file_="alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", db)
    alembic_upgrade(alembic_config, "head")
