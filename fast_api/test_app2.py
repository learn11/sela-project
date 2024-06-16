import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from app import app, Customer, Product  # Assuming your FastAPI app is in main.py

client = TestClient(app)

# Test the GET /customers endpoint
def test_get_customers():
    response = client.get("/costumers")
    assert response.status_code == 500


# Test the GET /product endpoint
def test_get_products():
    response = client.get("/product")
    assert response.status_code == 500


# Test the POST /input endpoint
def test_create_customer():
    customer = {
        "name": "John Doe",
        "mail": "johndoe@example.com",
        "phone": "1234567890"
    }
    response = client.post("/input", json=customer)
    assert response.status_code == 555


# Test the POST /input_product endpoint
def test_create_product():
    products = [
        {
            "id": "1",
            "name": "Product 1",
            "provider": "Provider 1"
        },
        {
            "id": "2",
            "name": "Product 2",
            "provider": "Provider 2"
        }
    ]
    response = client.post("/input_product", json=products)
    assert response.status_code == 555
   

# Test the POST /delete endpoint
def test_delete_customer():
    customer = {
        "name": "John Doe",
        "mail": "johndoe@example.com",
        "phone": "1234567890"
    }
    response = client.post("/delete", json=customer)
    assert response.status_code == 405
    

# Test the POST /update endpoint
def test_update_customer():
    customer = {
        "name": "John Doe",
        "mail": "johndoe@example.com",
        "phone": "0987654321"
    }
    response = client.post("/update", json=customer)
    assert response.status_code == 500
    assert "updated_customer" in response.json()

# Run the tests
if __name__ == "__main__":
    pytest.main()
