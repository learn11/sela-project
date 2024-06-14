import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from main import app, MONGO_DB_NAME

# Test client for FastAPI
client = TestClient(app)

# Configuration for MongoDB (replace with your test configuration if needed)
MONGO_DB_USERNAME = 'root'
MONGO_DB_PASSWORD = 'edmon'
MONGO_DB_HOST = 'mongodb'
MONGO_DB_PORT = 27017
MONGO_DB_NAME_TEST = f"{MONGO_DB_NAME}_test"

# Connect to the test database
client_mongo = MongoClient(f"mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOST}")
db = client_mongo[MONGO_DB_NAME_TEST]

# Fixture to set up and tear down the database
@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    # Set up: Clear the database before each test
    db.customers.delete_many({})
    db.products.delete_many({})

    yield

    # Tear down: Clear the database after each test
    db.customers.delete_many({})
    db.products.delete_many({})

def test_create_customer():
    response = client.post("/input", json={"name": "John Doe", "mail": "john.doe@example.com", "phone": "1234567890"})
    assert response.status_code == 200
    assert response.json() == {"message": "Customer created successfully."}

    # Verify the customer was inserted in the database
    customer = db.customers.find_one({"mail": "john.doe@example.com"})
    assert customer is not None
    assert customer["name"] == "John Doe"
    assert customer["phone"] == "1234567890"

def test_get_customers():
    # Insert a customer into the database
    db.customers.insert_one({"name": "John Doe", "mail": "john.doe@example.com", "phone": "1234567890"})

    response = client.get("/costumers")
    assert response.status_code == 200
    assert response.json() == {
        "table": [
            {"name": "John Doe", "mail": "john.doe@example.com", "phone": "1234567890"}
        ]
    }

def test_create_product():
    response = client.post("/input_product", json=[{"id": "1", "name": "Product 1", "provider": "Provider A"}])
    assert response.status_code == 200
    assert response.json() == {"message": "Products created successfully."}

    # Verify the product was inserted in the database
    product = db.products.find_one({"id": "1"})
    assert product is not None
    assert product["name"] == "Product 1"
    assert product["provider"] == "Provider A"

def test_get_products():
    # Insert a product into the database
    db.products.insert_one({"id": "1", "name": "Product 1", "provider": "Provider A"})

    response = client.get("/product")
    assert response.status_code == 200
    assert response.json() == {
        "table": [
            {"id": "1", "name": "Product 1", "provider": "Provider A"}
        ]
    }

def test_delete_customer():
    # Insert a customer into the database
    db.customers.insert_one({"name": "John Doe", "mail": "john.doe@example.com", "phone": "1234567890"})

    response = client.post("/delete", json={"name": "John Doe", "mail": "john.doe@example.com", "phone": "1234567890"})
    assert response.status_code == 200
    assert response.json() == {"message": "Customer delete successfully."}

    # Verify the customer was deleted from the database
    customer = db.customers.find_one({"mail": "john.doe@example.com"})
    assert customer is None

def test_update_customer():
    # Insert a customer into the database
    db.customers.insert_one({"name": "John Doe", "mail": "john.doe@example.com", "phone": "1234567890"})

    response = client.post("/update", json={"name": "John Doe", "mail": "john.doe@example.com", "phone": "0987654321"})
    assert response.status_code == 200
    assert response.json()["message"] == "Customer updated successfully."

    # Verify the customer was updated in the database
    customer = db.customers.find_one({"mail": "john.doe@example.com"})
    assert customer is not None
    assert customer["phone"] == "0987654321"

if __name__ == "__main__":
    pytest.main()
