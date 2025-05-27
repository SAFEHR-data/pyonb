"""OCR API Server."""

import datetime
import logging

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, RedirectResponse

from .routers import marker, sparrow

logging.basicConfig(
    filename="pyonb-" + datetime.datetime.now(datetime.UTC).strftime("%Y_%m_%d") + ".log",
    format="%(asctime)s %(message)s",
    filemode="a",
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})

app.include_router(sparrow.router)
app.include_router(marker.router)


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    """Redirect localhost:<PORT> to Swagger at localhost:<PORT>/docs."""
    return RedirectResponse(url="/docs")


@app.get("/")
async def health_check() -> JSONResponse:
    """
    Health check endpoint to verify API is accessible.

    Returns 200 OK status if API is running properly.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"service": "pyonb-ocr-api", "status": "healthy"},
    )
