FROM python:3.12.8-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.8.12 /uv /uvx /bin/

# Install curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Move in server folder
WORKDIR /server

# Copy requirements.txt and install all dependencies
COPY requirements.txt ./
RUN uv pip install --no-cache-dir --system --index-strategy unsafe-best-match -r requirements.txt

# Copy all files in server directory
COPY . .

# Remove tmp files and uv
RUN rm -rf /tmp/* \
    && rm -rf /usr/uv \
    && rm -rf /usr/uvx

## Create no-root user
RUN useradd -m beuser && usermod -aG beuser beuser

# Set the no-root user
USER beuser:beuser

# Run FastAPI application
CMD ["uvicorn", "app.app:app", "--host=0.0.0.0", "--port=30010", "--log-level=info", "--timeout-keep-alive=180"]