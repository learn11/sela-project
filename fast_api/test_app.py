from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_customers():
    response = client.get("/customers")
    assert response.status_code == 200

def test_get_products():
    response = client.get("/product")
    assert response.status_code == 200

def test_create_and_delete_customer():
    # Create a customer
    response = client.post("/input", json={"name": "John", "mail": "john@example.com", "phone": "123456789"})
    assert response.status_code == 200
    assert response.json() == {"message": "Customer created successfully."}
    
    # Fetch the created customer's ID (assuming the response has an ID or we can fetch the customer list to get the ID)
    response = client.get("/customers")
    assert response.status_code == 200
    customers = response.json()
    customer = next((c for c in customers if c['mail'] == "john@example.com"), None)
    assert customer is not None
    customer_id = customer['id']
    
    # Delete the customer
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Customer deleted successfully."}
