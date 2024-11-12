"""
Main module for the FastAPI application.
"""

from fastapi import FastAPI
from app.api.v1.endpoints.calculator import router as calculator_router

app = FastAPI()

app.include_router(calculator_router, prefix="/api/v1", tags=["calculator"])
