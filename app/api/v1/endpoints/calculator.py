from fastapi import APIRouter, HTTPException, Query  
from pydantic import BaseModel  
  
router = APIRouter()  
  
class Operation(BaseModel):  
    operand1: float  
    operand2: float  
  
@router.post("/add")  
def add(operation: Operation):  
    return {"result": operation.operand1 + operation.operand2}  
  
@router.post("/subtract")  
def subtract(operation: Operation):  
    return {"result": operation.operand1 - operation.operand2}  
  
@router.post("/multiply")  
def multiply(operation: Operation):  
    return {"result": operation.operand1 * operation.operand2}  
  
@router.post("/divide")  
def divide(operation: Operation):  
    if operation.operand2 == 0:  
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")  
    return {"result": operation.operand1 / operation.operand2}  
