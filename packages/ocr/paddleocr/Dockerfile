FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS app

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]


RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update \
    && apt-get install -y --no-install-recommends \
       ccache \
       cmake \
       curl \
       ffmpeg \
       libpoppler-cpp-dev \
       libsm6 \
       libxext6 \
       pkg-config \
       poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./pyproject.toml .
COPY ./README.md .
COPY ./src src/

RUN uv venv
RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked uv sync --no-editable --no-dev

# make uvicorn etc available
ENV PATH="/app/.venv/bin:$PATH"

CMD uvicorn pyonb_paddleocr.api:app --host 0.0.0.0 --port "$PADDLEOCR_API_PORT" --workers 4 --use-colors
