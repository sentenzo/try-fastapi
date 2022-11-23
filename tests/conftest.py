import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from service.__main__ import make_app
from service.config import get_config
from service.database import Base, get_db


engine = create_engine(get_config().test_database_url)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    # from alembic import command

    # command.downgrade("base")
    # command.upgrade("head")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def get_test_db():
        yield session

    app = make_app()
    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)
