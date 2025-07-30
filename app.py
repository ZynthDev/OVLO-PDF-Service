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
        user_id=data.get("user_id", ""),
        date=data.get("date", ""),
        tracking_since=data.get("tracking_since", ""),
        average_cycle_length=data.get("average_cycle_length", ""),
        average_period_duration=data.get("average_period_duration", ""),
        logged_cycles=data.get("logged_cycles", ""),
        most_common_symptom=data.get("most_common_symptom", ""),
        most_frequent_mood=data.get("most_frequent_mood", ""),
        longest_cycle=data.get("longest_cycle", ""),
        shortest_cycle=data.get("shortest_cycle", ""),
        cycle_history=data.get("cycle_history", []),
        symptom_logs=data.get("symptom_logs", []),
        mood_logs=data.get("mood_logs", []),
        most_common_symptoms=data.get("most_common_symptoms", []),
        mood_distribution=data.get("mood_distribution", []),
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
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=True)


