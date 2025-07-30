# ====================
# Stage 1: Build Layer
# ====================
FROM python:3.10-slim AS build

LABEL stage="build"

USER root

# Install build dependencies and minimal fonts
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    fontconfig \
    fonts-noto-color-emoji \
 && chmod -R a+r /usr/share/fonts \
 && fc-cache -f -v \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 user
USER user

# Set up environment
ENV PATH="/home/user/.local/bin:$PATH"
WORKDIR /app

# Install Python dependencies
COPY --chown=user ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --no-compile --user -r requirements.txt

# Copy full app source code (excluding .venv via .dockerignore)
COPY --chown=user . /app

# Clean build env (pycache, .pyc)
RUN find /home/user/.local -type d -name "__pycache__" -exec rm -rf {} + \
 && find /home/user/.local -type f -name "*.py[co]" -delete


# ====================
# Stage 2: Final Slim Runtime
# ====================
FROM python:3.10-slim AS runtime

LABEL rebuild="2025-07-30"

USER root

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    curl \
    fontconfig \
    fonts-noto-color-emoji \
 && chmod -R a+r /usr/share/fonts \
 && fc-cache -f -v \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 user
USER user

# Set up environment
ENV PATH="/home/user/.local/bin:$PATH"
WORKDIR /app

# Copy user packages and app from build stage
COPY --from=build --chown=user /home/user/.local /home/user/.local
COPY --from=build --chown=user /app /app

# Extra cleanup just in case
RUN rm -rf /app/.venv \
 && find /home/user/.local -type d -name "__pycache__" -exec rm -rf {} + \
 && find /home/user/.local -type f -name "*.py[co]" -delete \
 && fc-cache -f -v

# Start the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
