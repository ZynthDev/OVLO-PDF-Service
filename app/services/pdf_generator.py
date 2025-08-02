from fastapi.responses import StreamingResponse
from weasyprint import HTML
from io import BytesIO
from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_DIR = os.path.join(os.getcwd(), "app/templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template("ovlo_template.html")

async def generate_pdf_from_html(file):
    html_bytes = await file.read()
    pdf_io = BytesIO()
    HTML(string=html_bytes.decode("utf-8")).write_pdf(target=pdf_io)
    pdf_io.seek(0)
    return StreamingResponse(pdf_io, media_type="application/pdf", status_code=201)

def generate_pdf_from_json_data(data):
    options = data.get("options", "111")
    if len(options) != 3 or not all(c in "01" for c in options):
        raise ValueError("Invalid options format. Must be a string like '110'.")

    data["show_cycles"] = options[0] == "1"
    data["show_symptoms"] = options[1] == "1"
    data["show_mood"] = options[2] == "1"

    rendered_html = template.render(**data)
    pdf_io = BytesIO()
    HTML(string=rendered_html).write_pdf(target=pdf_io)
    pdf_io.seek(0)
    return StreamingResponse(pdf_io, media_type="application/pdf", status_code=201)

