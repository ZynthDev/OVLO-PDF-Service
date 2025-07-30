from fastapi import APIRouter, Request
from app.services.csv_generator import generate_csv_zip_from_json

router = APIRouter()

@router.post("/generate")
async def generate_csv_zip(request: Request):
    data = await request.json()
    return generate_csv_zip_from_json(data)
