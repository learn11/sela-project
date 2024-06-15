

from fastapi import FastAPI
from fastapi.testclient import TestClient

# === FastAPI Application ===

app = FastAPI()

# Sample endpoint to create a customer
@app.post("/input")
def create_customer(name: str, mail: str, phone: str):
    # Example: Simulate insert into MongoDB (in reality, we mock this)
    return {"message": "Customer created successfully."}

# === Tests ===

client = TestClient(app)

def test_create_customer():
    response = client.post("/input", json={"name": "John Doe", "mail": "john.doe@example.com", "phone": "1234567890"})
    assert response.status_code == 200
    assert response.json() == {"message": "Customer created successfully."}

# Running pytest if executed directly
if __name__ == "__main__":
    import pytest
    pytest.main()
