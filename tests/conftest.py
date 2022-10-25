import os
from uuid import uuid4

import pytest
import dotenv
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlalchemy.ext.asyncio import AsyncSession
from alembic.command import upgrade as alembic_upgrade, downgrade as alembic_downgrade
from alembic.config import Config as AlembicConfig
from fastapi.testclient import TestClient


from tryFastAPI.db.connection.session import DbUriBuilderLocal
from tryFastAPI import make_app
from tryFastAPI.db.connection.session import get_session_dependency


dotenv.load_dotenv()


@pytest.fixture(scope="session")
def env():
    prev_db_name = None
    try:
        prev_db_name = os.environ["DB_DBNAME"]
        tmp_db_name = f"{prev_db_name}-pytest-{uuid4().hex}"
        os.environ["DB_DBNAME"] = tmp_db_name
        yield
    finally:
        os.environ["DB_DBNAME"] = prev_db_name


@pytest.fixture(scope="session")
def db(env) -> str:
    tmp_db_url = None
    try:
        url_builder = DbUriBuilderLocal().from_env()
        tmp_db_url = url_builder.to_str()
        tmp_db_url_sync = url_builder.driver(None).to_str()
        if not database_exists(tmp_db_url_sync):
            create_database(tmp_db_url_sync)
            yield tmp_db_url
    finally:
        if tmp_db_url_sync and database_exists(tmp_db_url_sync):
            drop_database(tmp_db_url_sync)
            ...


@pytest.fixture(scope="class")
def migrated_db(db):
    alembic_config = AlembicConfig(file_="alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", db)
    alembic_upgrade(alembic_config, "head")
    yield
    alembic_downgrade(alembic_config, "base")


@pytest.fixture
async def acync_session(env, migrated_db):
    async for session in get_session_dependency():
        yield session


@pytest.fixture
def client() -> TestClient:
    app = make_app()
    return TestClient(app)
