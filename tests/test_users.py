from uuid import UUID

import pytest
from fastapi import status

from service import oauth2
from service.schemas.misc import Token, TokenData
from service.schemas.user import UserResponse


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


def test_get_user(client, test_users: list[tuple[UserResponse, dict]]):
    for user, _ in test_users:
        result = client.get(f"/user/{user.id}")
        assert result.status_code == status.HTTP_200_OK
        db_user = UserResponse(**result.json())
        assert db_user.email == user.email
        assert db_user.id == user.id


def test_get_all_user(client, test_users: list[tuple[UserResponse, dict]]):
    result = client.get("/user/all")
    assert result.status_code == status.HTTP_200_OK
    result_json = result.json()
    assert len(result_json) == len(test_users)
    user_ids = {user.id for user, _ in test_users}
    for user in result_json:
        assert UUID(user["id"]) in user_ids


def test_login_user(client, test_users: list[tuple[UserResponse, dict]]):
    for user, user_dicr in test_users:
        password = user_dicr["password"]
        result = client.post(
            "/auth/login",
            data={
                "username": user.email,
                "password": password,
            },
        )
        assert result.status_code == status.HTTP_200_OK

        auth_result = Token(**result.json())
        assert auth_result.token_type == "bearer"
        token_data: TokenData = oauth2.verify_access_token(auth_result.token)
        assert token_data.id == user.id


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        (
            TEST_USERS[0]["email"],
            TEST_USERS[0]["password"] + "*",
            status.HTTP_401_UNAUTHORIZED,
        ),
        (
            TEST_USERS[0]["email"] + "x",
            TEST_USERS[0]["password"],
            status.HTTP_401_UNAUTHORIZED,
        ),
        (
            TEST_USERS[0]["email"] + "x",
            TEST_USERS[0]["password"] + "*",
            status.HTTP_401_UNAUTHORIZED,
        ),
        ("", TEST_USERS[0]["password"], status.HTTP_422_UNPROCESSABLE_ENTITY),
        (TEST_USERS[0]["email"], "", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
def test_login_user_fail(
    client,
    test_users: list[tuple[UserResponse, dict]],
    email,
    password,
    status_code,
):
    result = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )
    assert result.status_code == status_code
