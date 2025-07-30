from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.routes import pdf, csv

app = FastAPI()
router = APIRouter()

# Optional: Add CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdf.router, prefix="/pdf", tags=["PDF"])
app.include_router(csv.router, prefix="/csv", tags=["CSV"])

@router.post("/")
async def root():
    return {
        "message": "Hello World"
    }

app.include_router(router)