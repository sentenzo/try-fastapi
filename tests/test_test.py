from fastapi.testclient import TestClient


def test(client: TestClient):
    response = client.put("/set/http", json={"key": "t0", "html": "<p>test 0</p>"})
    assert response.status_code == 200
    response = client.get("/get/http/t0")
    assert response.status_code == 200
