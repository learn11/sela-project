# Combined file structure: app_with_tests.py

# === FastAPI Application ===

from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

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

# === Tests ===

import pytest
from fastapi.testclient import TestClient

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

# Tests

def test_create_customer():
    response = client.post("/input", json={"name": "John Doe", "mail": "john.doe@example.com", "phone": "1234567890"})
    assert response.status_code == 200
    assert response.json() == {"message": "Customer created successfully."}

    # Verify the customer was inserted in the database
    customer = db.customers.find_one({"mail": "john.doe@example.com"})
    assert customer is not None
    assert customer["name"] == "John Doe"
    assert customer["phone"] == "1234567890"

# Running pytest if executed directly
if __name__ == "__main__":
    pytest.main()
