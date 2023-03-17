from fastapi import APIRouter
from src.endpoints import model_endpoint

api_router = APIRouter(prefix="/api")
api_router.include_router(model_endpoint.router, prefix="/model", tags=["Model"])
