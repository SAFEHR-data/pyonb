"""OCR API Server."""

import datetime
import logging

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from .routers import marker, sparrow, paddleocr

logging.basicConfig(
    filename="pyonb-" + datetime.datetime.now(datetime.UTC).strftime("%Y_%m_%d") + ".log",
    format="%(asctime)s %(message)s",
    filemode="a",
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = FastAPI()

app.include_router(sparrow.router)
app.include_router(marker.router)
app.include_router(paddleocr.router)


# Creating an object
logger = logging.getLogger()


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
