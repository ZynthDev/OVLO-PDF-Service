from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import StreamingResponse
from app.services.pdf_generator import generate_pdf_from_html, generate_pdf_from_json_data

router = APIRouter()

@router.post("/generate-from-file")
async def generate_pdf(file: UploadFile = File(...)):
    return await generate_pdf_from_html(file)

@router.post("/generate-from-json")
async def generate_pdf_json(request: Request):
    data = await request.json()
    return generate_pdf_from_json_data(data)
