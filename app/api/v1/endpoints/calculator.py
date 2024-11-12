"""Calculator API endpoints using FastAPI."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class Operation(BaseModel):
    """Model for arithmetic operations."""
    operand1: float
    operand2: float

@router.post("/add")
def add(operation: Operation):
    """Endpoint to add two numbers."""
    return {"result": operation.operand1 + operation.operand2}

@router.post("/subtract")
def subtract(operation: Operation):
    """Endpoint to subtract two numbers."""
    return {"result": operation.operand1 - operation.operand2}

@router.post("/multiply")
def multiply(operation: Operation):
    """Endpoint to multiply two numbers."""
    return {"result": operation.operand1 * operation.operand2}

@router.post("/divide")
def divide(operation: Operation):
    """Endpoint to divide two numbers."""
    if operation.operand2 == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")
    return {"result": operation.operand1 / operation.operand2}
