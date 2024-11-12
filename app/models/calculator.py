"""Model for arithmetic operations."""

from pydantic import BaseModel

class Operation(BaseModel):
    """Model for arithmetic operations."""
    operand1: float
    operand2: float
