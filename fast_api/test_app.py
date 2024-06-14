from fastapi.testclient import TestClient
from app import app

client = TestClient(app, base_url="http://127.0.0.1:8000")

def test_create_and_delete_customer():
    # Create a customer
    customer_data = {"name": "John", "mail": "john@example.com", "phone": "123456789"}
    response = client.post("/input", json=customer_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Customer created successfully."}
    
    # Fetch the created customer's ID
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

def test_get_customers():
    response = client.get("/customers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_and_get_product():
    # Create a product
    product_data = {"id": "1", "name": "Laptop", "provider": "ProviderA"}
    response = client.post("/input_product", json=[product_data])
    assert response.status_code == 200
    assert response.json() == {"message": "Products created successfully."}
    
    # Fetch the created product
    response = client.get("/product")
    assert response.status_code == 200
    products = response.json()
    product = next((p for p in products if p['name'] == "Laptop"), None)
    assert product is not None
