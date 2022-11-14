import pytest
from fastapi import status

from service.schemas.user import UserResponse
from service.schemas.misc import Token


class TestUserEntity:
    users_to_create = [
        {"email": "test000@test.com", "password": "hack me"},
        {"email": "test001@test.com", "password": "hack me"},
        {"email": "test002@test.com", "password": "hack me"},
        {"email": "test003@test.com", "password": "hack me"},
    ]

    def test_create_user(self, client):
        for user_dict in TestUserEntity.users_to_create:
            result = client.post("/user", json=user_dict)
            assert result.status_code == status.HTTP_201_CREATED
            new_user = UserResponse(**result.json())
            assert new_user.email == user_dict["email"]
            user_dict["id"] = new_user.id

    def get_user(self, client):
        for user_dict in TestUserEntity.users_to_create:
            result = client.get(f"/user/{user_dict['id']}")
            assert result.status_code == status.HTTP_200_OK
            db_user = UserResponse(**result.json())
            assert db_user.email == user_dict["email"]
            assert db_user.id == user_dict["id"]

    def get_all_user(self, client):
        result = client.get("/user/all")
        assert result.status_code == status.HTTP_200_OK
        result_json = result.json()
        assert len(result_json) == len(TestUserEntity.users_to_create)
        user_ids = {u["id"] for u in TestUserEntity.users_to_create}
        for user_dict in result_json:
            user = UserResponse(**user_dict.json())
            assert user.id in user_ids

    def test_login_user(self, client):
        for user_dict in TestUserEntity.users_to_create:
            result = client.post(
                "/auth/login",
                data={
                    "username": user_dict["email"],
                    "password": user_dict["password"],
                },
            )
            assert result.status_code == status.HTTP_200_OK
            auth_result = Token(**result.json())
            user_dict["token"] = auth_result.token
