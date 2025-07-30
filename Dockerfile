FROM python:3.10

# Force rebuild (cache busting for Hugging Face)
LABEL rebuild="2025-07-30"

# Install font packages as root
USER root

RUN apt-get update && apt-get install -y \
    fonts-noto-color-emoji \
    fonts-noto-core \
    fonts-dejavu-core \
    fontconfig \
 && fc-cache -f -v \
 && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 user
USER user

# Rebuild font cache as user to ensure visibility
RUN fc-cache -f -v

ENV PATH="/home/user/.local/bin:$PATH"
WORKDIR /app

# Install Python dependencies
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the app
COPY --chown=user . /app

# Default command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
