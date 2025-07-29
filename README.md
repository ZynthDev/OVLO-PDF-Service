## OVLO PDF Service

OVLO PDF Service is a microservice designed to generate PDFs from HTML or JSON input, suitable for rendering templates and exporting user data in a visually appealing format. It utilizes FastAPI along with WeasyPrint and Jinja2 for rendering and generating PDFs.

### Features

- Convert uploaded HTML files to PDF.
- Generate PDF from JSON data using pre-defined HTML templates.
- RESTful endpoints for handling PDF generation.
- Dockerized for seamless deployment and scalability.

### Installation

#### Prerequisites

- **Python 3.10+**: Ensure Python is installed on your system.
- **Docker**: Required for running the microservice in a containerized environment.

#### Steps

1. **Clone the repository**: 
   ```bash
   git clone <repository-url>
   cd OVLO-PDF-Service
   ```

2. **Install dependencies**: 
   Using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Build Docker Image**:
   ```bash
   docker build -t ovlo-pdf-service .
   ```

### Usage

Run the service locally using Uvicorn:
```bash
uvicorn app:app --reload
```

Run using Docker:
```bash
docker run -p 7860:7860 ovlo-pdf-service
```

### API Endpoints

- **GET /**: Welcome message discussing functionalities.
- **POST /generate-pdf**: Upload an HTML file to generate a PDF.
- **POST /generate-pdf-from-json**: Send JSON data to create a PDF based on the `ovlo_template.html`.

### Template Customization

Modify `ovlo_template.html` to match your visual and data structure requirements. The template is powered by Jinja2 allowing dynamic rendering based on provided data.

### License

MIT License - see [LICENSE](LICENSE) file for details.
