import pytest
from fastapi import status


@pytest.mark.parametrize(
    "url", ["/healthcheck/ping_app", "/healthcheck/ping_db"]
)
def test_ping(client, url):
    assert client.get(url).status_code == status.HTTP_200_OK
