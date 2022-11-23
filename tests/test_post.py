import pytest
from fastapi import status


def test_get_post_all(authorized_client):
    result = authorized_client.get("/post/all")
    print(result.json())
    assert result.status_code == status.HTTP_200_OK
