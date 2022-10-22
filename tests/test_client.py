from fastapi.testclient import TestClient

def test_ping(client: TestClient):
    response = client.get("/ping/app")
    assert response.status_code == 200


def test_ping_db(db, client: TestClient):
    response = client.get("/ping/db")
    assert response.status_code == 200


class TestHtmlEndpoint:
    @property
    def in_json(self):
        return {"key": "t0", "html": "<p>test 0</p>"}

    def test_html_put(self, migrated_db, client: TestClient):
        response = client.put("/http", json=self.in_json)
        assert response.status_code == 200
        assert response.json() == self.in_json

        response = client.put("/http", json=self.in_json)
        assert response.status_code == 409

    def test_html_get(self, migrated_db, client: TestClient):
        key = self.in_json["key"]
        response = client.get(f"/http/{key}")
        assert response.status_code == 200
        assert response.json() == self.in_json

        response = client.get("/http/NO_SUCH_KEY")
        assert response.status_code == 404

    def test_html_post(self, migrated_db, client: TestClient):
        json = self.in_json
        json["html"] += " - changed"
        response = client.post(f"/http", json=json)
        assert response.status_code == 200
        assert response.json() == json

        json["key"] = "NO_SUCH_KEY"
        response = client.post("/http", json=json)
        assert response.status_code == 404

    def test_html_delete(self, migrated_db, client: TestClient):
        json = self.in_json
        key = json["key"]
        response = client.delete(f"/http/{key}")
        assert response.status_code == 200

        response = client.delete(f"/http/{key}")
        assert response.status_code == 404
