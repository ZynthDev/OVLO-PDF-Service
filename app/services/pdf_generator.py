from fastapi.responses import StreamingResponse
from weasyprint import HTML
from io import BytesIO
from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_DIR = os.path.join(os.getcwd(), "app", "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template("ovlo_template.html")

async def generate_pdf_from_html(file):
    html_bytes = await file.read()
    pdf_io = BytesIO()
    HTML(string=html_bytes.decode("utf-8")).write_pdf(target=pdf_io)
    pdf_io.seek(0)
    return StreamingResponse(pdf_io, media_type="application/pdf")

def generate_pdf_from_json_data(data):
    rendered_html = template.render(**data)
    pdf_io = BytesIO()
    HTML(string=rendered_html).write_pdf(target=pdf_io)
    pdf_io.seek(0)
    return StreamingResponse(pdf_io, media_type="application/pdf")
