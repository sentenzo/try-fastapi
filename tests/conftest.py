import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from service import oauth2
from service.__main__ import make_app
from service.config import get_config
from service.database import Base, get_db
from service.schemas.user import UserResponse


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
def client(session) -> TestClient:
    def get_test_db():
        yield session

    app = make_app()
    app.dependency_overrides[get_db] = get_test_db
    return TestClient(app)


TEST_USERS = [
    {"email": "test000@test.com", "password": "hack me"},
    {"email": "test001@test.com", "password": "hack me"},
    # {"email": "test002@test.com", "password": "hack me"},
    # {"email": "test003@test.com", "password": "hack me"},
]


@pytest.fixture
def test_users(client) -> list[tuple[UserResponse, dict]]:
    users = []
    for user_dict in TEST_USERS:
        result = client.post("/user", json=user_dict)
        assert result.status_code == status.HTTP_201_CREATED
        new_user = UserResponse(**result.json())
        assert new_user.email == user_dict["email"]
        users.append((new_user, user_dict))
    return users


@pytest.fixture
def token(test_users):
    user, _ = test_users[0]
    return oauth2.create_access_token({"user_id": str(user.id)})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client
