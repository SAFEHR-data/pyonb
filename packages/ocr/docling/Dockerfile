FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS app

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

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

CMD uvicorn pyonb_docling.api:app --host 0.0.0.0 --port "$DOCLING_API_PORT" --workers 4 --use-colors
