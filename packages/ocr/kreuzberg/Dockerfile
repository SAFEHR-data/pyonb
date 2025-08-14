FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS app

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./pyproject.toml ./README.md .
COPY ./src src/

RUN uv venv
RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked uv sync --no-editable --no-dev --compile-bytecode

# make uvicorn etc available
ENV PATH="/app/.venv/bin:$PATH"

CMD uvicorn kreuzberg._api.main:app --host 0.0.0.0 --port "$KREUZBERG_API_PORT" --workers 4 --reload --use-colors

