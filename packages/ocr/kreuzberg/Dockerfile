FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS app

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    pandoc \
    tesseract-ocr \
    tesseract-ocr-eng \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./pyproject.toml ./README.md .
COPY ./src src/

RUN uv venv
RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked uv sync --no-editable --no-dev

# make uvicorn etc available
ENV PATH="/app/.venv/bin:$PATH"

CMD uvicorn pyonb_kreuzberg.api:app --host 0.0.0.0 --port "$KREUZBERG_API_PORT" --workers 4 --reload --use-colors
