---
title: OVLO Conversion Service
emoji: 🐨
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: 5.38.2
app_file: app.py
pinned: false
license: mit
---

> Check out the configuration reference at [huggingface.co/docs/hub/spaces-config-reference](https://huggingface.co/docs/hub/spaces-config-reference)

# 🧾 OVLO PDF Service

The **OVLO PDF Service** is a microservice designed to generate high-quality PDFs from HTML or structured JSON data. It’s perfect for rendering user data, reports, or logs into printable formats using Jinja2 templating and WeasyPrint.

---

## ✨ Features

- 📄 Convert uploaded HTML files directly to PDF
- 🧩 Generate dynamic PDFs from JSON using pre-defined templates
- ⚙️ RESTful FastAPI endpoints for easy integration
- 🐳 Docker support for quick deployment and scaling

---

## 🚀 Getting Started

### 🧰 Prerequisites

- Python 3.10+
- Docker (optional, for containerized use)

---

### 🔧 Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd OVLO-PDF-Service