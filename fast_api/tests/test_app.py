

from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
import pytest
from fastapi.testclient import TestClient

# === FastAPI Application ===

app = FastAPI()

# MongoDB configuration
MONGO_DB_USERNAME = 'root'
MONGO_DB_PASSWORD = 'edmon'
MONGO_DB_HOST = 'mongodb'
MONGO_DB_PORT = 27017
MONGO_DB_NAME = 'mydb'
MONGO_DB_NAME_TEST = f"{MONGO_DB_NAME}_test"

# MongoDB client
client = MongoClient(f"mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOST}:{MONGO_DB_PORT}/")
db = client[MONGO_DB_NAME]

# Sample endpoint to create a customer
@app.post("/input")
def create_customer(name: str, mail: str, phone: str):
    # Example: Insert into MongoDB
    result = db.customers.insert_one({
        "name": name,
        "mail": mail,
        "phone": phone
    })
    return {"message": "Customer created successfully."}

# Endpoint to update customer information
@app.put("/update")
def update_customer(mail: str, name: str, phone: str):
    # Update customer details in MongoDB
    result = db.customers.update_one(
        {"mail": mail},
        {"$set": {"name": name, "phone": phone}}
    )
    if result.modified_count == 1:
        return {"message": "Customer updated successfully."}
    else:
        raise HTTPException(status_code=404, detail="Customer not found")

# New endpoint to get customer details by email
@app.get("/customer")
def get_customer_by_email(email: str = Query(...)):
    customer = db.customers.find_one({"mail": email})
    if customer:
        return customer
    else:
        raise HTTPException(status_code=404, detail="Customer not found")

# === Pytest Fixtures and Tests ===

# FastAPI TestClient
client = TestClient(app)

# MongoDB Test Configuration
@pytest.fixture(scope="module")
def mongo_client():
    client = MongoClient(f"mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOST}:{MONGO_DB_PORT}/")
    yield client

@pytest.fixture(scope="module")
def mongo_database(mongo_client):
    db = mongo_client[MONGO_DB_NAME_TEST]
    yield db

@pytest.fixture(autouse=True)
def setup_and_teardown_db(mongo_database):
    # Set up: Clear the database before each test
    mongo_database.customers.delete_many({})
    mongo_database.products.delete_many({})

    yield

    # Tear down: Clear the database after each test
    mongo_database.customers.delete_many({})
    mongo_database.products.delete_many({})

# Custom test helper to create a customer
def create_test_customer(client: TestClient, name: str, mail: str, phone: str):
    return client.post("/input", json={"name": name, "mail": mail, "phone": phone})

# Custom test helper to update a customer
def update_test_customer(client: TestClient, mail: str, name: str, phone: str):
    return client.put("/update", json={"mail": mail, "name": name, "phone": phone})

# Custom test helper to retrieve a customer
def get_test_customer(client: TestClient, email: str):
    return client.get("/customer", params={"email": email})

# Tests using custom helpers
def test_create_customer():
    response = create_test_customer(client, "John Doe", "john.doe@example.com", "1234567890")
    assert response.status_code == 200
    assert response.json() == {"message": "Customer created successfully."}

    # Verify the customer was inserted in the database
    customer = db.customers.find_one({"mail": "john.doe@example.com"})
    assert customer is not None
    assert customer["name"] == "John Doe"
    assert customer["phone"] == "1234567890"

def test_update_customer():
    # Insert a test customer
    create_test_customer(client, "Jane Smith", "jane.smith@example.com", "9876543210")

    # Test updating customer details
    response = update_test_customer(client, "jane.smith@example.com", "Jane Doe", "5555555555")
    assert response.status_code == 200
    assert response.json() == {"message": "Customer updated successfully."}

    # Verify the customer was updated in the database
    updated_customer = db.customers.find_one({"mail": "jane.smith@example.com"})
    assert updated_customer is not None
    assert updated_customer["name"] == "Jane Doe"
    assert updated_customer["phone"] == "5555555555"
