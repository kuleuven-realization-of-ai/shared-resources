from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "People"}


def test_get_prediction():
    response = client.get("/get_prediction?feature_a=123&feature_b=12")
    assert response.status_code == 200

    output_payload_keys = list(response.json().keys())
    assert "predictions" in output_payload_keys
