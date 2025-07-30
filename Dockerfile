# ====================
# Stage 1: Build Layer
# ====================
FROM python:3.10-slim AS build

LABEL stage="build"

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    fontconfig \
    fonts-noto-color-emoji \
 && chmod -R a+r /usr/share/fonts \
 && fc-cache -f -v \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user
USER user

ENV PATH="/home/user/.local/bin:$PATH"
WORKDIR /app

COPY --chown=user ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --no-compile --user -r requirements.txt

COPY --chown=user . /app

RUN find /home/user/.local -type d -name "__pycache__" -exec rm -rf {} + \
 && find /home/user/.local -type f -name "*.py[co]" -delete


# ====================
# Stage 2: Final Slim Runtime
# ====================
FROM python:3.10-slim AS runtime

LABEL rebuild="2025-07-30"

USER root

RUN apt-get update && apt-get install -y \
    curl \
    fontconfig \
    fonts-noto-color-emoji \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libglib2.0-0 \
 && chmod -R a+r /usr/share/fonts \
 && fc-cache -f -v \
 && apt-get clean && rm -rf /var/lib/apt/lists/*


RUN useradd -m -u 1000 user
USER user

ENV PATH="/home/user/.local/bin:$PATH"
WORKDIR /app

COPY --from=build --chown=user /home/user/.local /home/user/.local
COPY --from=build --chown=user /app /app

RUN rm -rf /app/.venv \
 && find /home/user/.local -type d -name "__pycache__" -exec rm -rf {} + \
 && find /home/user/.local -type f -name "*.py[co]" -delete \
 && fc-cache -f -v

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]

