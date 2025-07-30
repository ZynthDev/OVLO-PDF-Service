FROM python:3.10

# Install font packages as root
USER root

RUN apt-get update && apt-get install -y \
    fonts-noto-color-emoji \
    fontconfig \
 && fc-cache -f -v \
 && rm -rf /var/lib/apt/lists/*

# Switch back to non-root user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user . /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
