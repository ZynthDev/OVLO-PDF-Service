from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi import Request
from io import BytesIO
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
import uvicorn

app = FastAPI()

# Load template engine
env = Environment(loader=FileSystemLoader("."))  # current directory
template = env.get_template("ovlo_template.html")

@app.get("/")
def read_root():
    return {"message": "Upload an HTML file or send JSON to get PDF."}

@app.post("/generate-pdf")
async def generate_pdf(file: UploadFile = File(...)):
    html_bytes = await file.read()
    html_str = html_bytes.decode("utf-8")

    pdf_io = BytesIO()
    HTML(string=html_str).write_pdf(target=pdf_io)
    pdf_io.seek(0)

    return StreamingResponse(
        pdf_io,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={file.filename.replace('.html', '.pdf')}"}
    )

@app.post("/generate-pdf-from-json")
async def generate_pdf_from_json(request: Request):
    data = await request.json()

    # Render HTML from template using data
    rendered_html = template.render(
        date=data.get("date", ""),
        customer=data.get("customer", {}),
        items=data.get("items", []),
        total=data.get("total", "0.00")
    )

    pdf_io = BytesIO()
    HTML(string=rendered_html).write_pdf(target=pdf_io)
    pdf_io.seek(0)

    return StreamingResponse(
        pdf_io,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=file.pdf"}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

