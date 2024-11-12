from fastapi.testclient import TestClient  
from app.main import app  
  
client = TestClient(app)  
  
def test_add():  
    response = client.post("/api/v1/add", json={"operand1": 5, "operand2": 3})  
    assert response.status_code == 200  
    assert response.json() == {"result": 8}  
  
def test_subtract():  
    response = client.post("/api/v1/subtract", json={"operand1": 5, "operand2": 3})  
    assert response.status_code == 200  
    assert response.json() == {"result": 2}  
  
def test_multiply():  
    response = client.post("/api/v1/multiply", json={"operand1": 5, "operand2": 3})  
    assert response.status_code == 200  
    assert response.json() == {"result": 15}  
  
def test_divide():  
    response = client.post("/api/v1/divide", json={"operand1": 6, "operand2": 3})  
    assert response.status_code == 200  
    assert response.json() == {"result": 2.0}  
  
def test_divide_by_zero():  
    response = client.post("/api/v1/divide", json={"operand1": 6, "operand2": 0})  
    assert response.status_code == 400  
    assert response.json() == {"detail": "Division by zero is not allowed"}  