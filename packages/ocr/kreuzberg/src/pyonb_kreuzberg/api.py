"""API for Kreuzberg OCR."""

import os

import uvicorn
from kreuzberg._api.main import (
    KreuzbergError,
    Litestar,
    OpenTelemetryConfig,
    OpenTelemetryPlugin,
    StructLoggingConfig,
    exception_handler,
    general_exception_handler,
    get_configuration,
    handle_files_upload,
    health_check,
)

KREUZBERG_API_PORT = int(os.getenv("KREUZBERG_API_PORT", default="8116"))

app = Litestar(
    route_handlers=[handle_files_upload, health_check, get_configuration],
    request_max_body_size=100_000_000,
    plugins=[OpenTelemetryPlugin(OpenTelemetryConfig())],
    logging_config=StructLoggingConfig(),
    exception_handlers={
        KreuzbergError: exception_handler,
        Exception: general_exception_handler,
    },
)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=KREUZBERG_API_PORT,
        workers=4,
        reload=True,
        use_colors=True,
    )
