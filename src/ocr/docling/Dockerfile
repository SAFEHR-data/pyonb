FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Add uv installer, run it, then remove it
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure installed uv binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Tell uv to use system Python environment by default
ENV UV_SYSTEM_PYTHON=1

COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt

COPY main.py api.py ./

CMD uvicorn api:app --host 0.0.0.0 --port $DOCLING_API_PORT
# ENTRYPOINT ["python", "main.py"]
