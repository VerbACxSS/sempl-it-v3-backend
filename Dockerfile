FROM bitnami/python:3.12.8
COPY --from=ghcr.io/astral-sh/uv:0.7.19 /uv /uvx /bin/

# Move in server folder
WORKDIR /server

# Copy requirements.txt and install all dependencies
COPY requirements.txt ./
RUN uv pip install --no-cache-dir --system --index-strategy unsafe-best-match -r requirements.txt

# Copy all files in server directory
COPY . .

# Clean up temporary files and directories
RUN rm -rf /tmp/* \
    && rm -rf /usr/uv \
    && rm -rf /usr/uvx

# Run FastAPI application
CMD ["uvicorn", "app.app:app", "--host=0.0.0.0", "--port=30010", "--log-level=info", "--workers=2", "--timeout-keep-alive=120"]