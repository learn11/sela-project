from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_customers():
    response = client.get("/customers")
    assert response.status_code == 200

def test_get_products():
    response = client.get("/product")
    assert response.status_code == 200

def test_create_customer():
    response = client.post("/input", json={"name": "John", "mail": "john@example.com", "phone": "123456789"})
    assert response.status_code == 200
    assert response.json() == {"message": "Customer created successfully."}
