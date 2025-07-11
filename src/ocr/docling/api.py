"""Docling API."""

import datetime
import logging
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse, RedirectResponse

logging.basicConfig(
    filename="docling." + datetime.datetime.now(tz=datetime.UTC).strftime("%Y%m%d") + ".log",
    format="%(asctime)s %(message)s",
    filemode="a",
)

# Creating an object
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# TODO(tom): improve imports - below try statements horrible
try:
    # local
    from .main import convert_pdf_to_markdown
except Exception:
    logger.exception("Detected inside Docker container.")
    # Docker container
    try:
        from main import convert_pdf_to_markdown  # type: ignore  # noqa: PGH003
    except Exception:
        logger.exception("Docling imports not possible.")

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    """Redirect localhost:<PORT> to Swagger at localhost:<PORT>/docs."""
    return RedirectResponse(url="/docs")


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> JSONResponse:
    """
    Health check endpoint to verify API is accessible.

    Returns 200 OK status if API is running properly.
    """
    logger.info("[POST] /health")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"service": "docling", "status": "healthy"},
    )


@app.post("/inference", status_code=status.HTTP_200_OK)
async def inference(file: Annotated[UploadFile, File()] = None) -> JSONResponse:
    """
    Endpoint to execute Docling on PDF file.

    Returns 200 OK JSON formatted text result from Docling.
    """
    logger.info("[POST] /inference")
    logger.info("[POST] /inference - Received file: %s", file.filename)

    result = None
    if file:
        if file.content_type == "application/pdf":
            try:
                content = await file.read()
                # Docling requires path to file rather than UploadFile object, so create temp copy of file
                with Path(f"temp_api_file_{file.filename}").open("wb") as f:  # noqa: ASYNC230
                    f.write(content)
                result = convert_pdf_to_markdown(f"temp_api_file_{file.filename}")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to run Docling. Error: {e}") from e
        else:
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF are allowed.")

    if result is None:
        raise HTTPException(status_code=400, detail="Failed to process the input.")

    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
