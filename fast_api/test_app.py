from fastapi.testclient import TestClient
from router import app
testclient = TestClient(app)



def test_list_of_costumers():
    respose = testclient.get("/costumers")
    assert respose.status_code == 200

def test_add_input_page():
    respose = testclient.get("/input")
    assert respose.status_code == 200

def test_add_costumer():
    form_data = {"name": "testname", "email": "email", "phone": "test number"}
    respose = testclient.post("/input", data=form_data)
    assert respose.status_code == 200

def test_add_product_page():
    respose = testclient.get("/input_product")
    assert respose.status_code == 200

def test_add_product():
    form_data = {"id": "test","name": "test", "provider": "test"}
    respose = testclient.post("/input_product", data=form_data)
    assert respose.status_code == 200



def test_update_costumer_page():
    respose = testclient.get("/update/company/testcompany")
    assert respose.status_code == 200

def test_update_costumer():
    form_data = {"name": "testcompany", "field": "testfield", "manager": "test manager", "phone": "updated test number"}
    respose = testclient.post("/update/company/testcompany", data=form_data)
    assert respose.status_code == 200

