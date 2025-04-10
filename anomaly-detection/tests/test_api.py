# Testes automatizados para a API
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "API Running"}
