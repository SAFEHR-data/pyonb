"""Marker API."""

import datetime
import logging
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

logging.basicConfig(
    filename="marker." + datetime.datetime.now(tz=datetime.UTC).strftime("%Y%m%d") + ".log",
    format="%(asctime)s %(message)s",
    filemode="a",
)

# Creating an object
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# TODO(tom): improve imports - below try statements horrible
try:
    # local
    from .main import run_marker
except Exception:
    logger.exception("Detected inside Docker container.")
    # Docker container
    try:
        from main import run_marker  # type: ignore  # noqa: PGH003
    except Exception:
        logger.exception("Marker imports not possible.")

app = FastAPI()


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> JSONResponse:
    """
    Health check endpoint to verify API is accessible.

    Returns 200 OK status if API is running properly.
    """
    logger.info("[POST] /health")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"service": "marker", "status": "healthy"},
    )


@app.post("/inference", status_code=status.HTTP_200_OK)
async def inference(file: Annotated[UploadFile, File()] = None) -> JSONResponse:
    """
    Endpoint to execute marker on PDF file.

    Returns 200 OK JSON formatted text result from marker.
    """
    logger.info("[POST] /inference")
    logger.info("[POST] /inference - Received file: %s", file.filename)

    result = None
    if file:
        if file.content_type == "application/pdf":
            try:
                content = await file.read()
                # marker requires path to file rather than UploadFile object
                with Path(f"temp_api_file_{file.filename}").open("wb") as f:  # noqa: ASYNC230
                    f.write(content)
                result, _ = run_marker(f"temp_api_file_{file.filename}")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to run marker. Error: {e}") from e
        else:
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF are allowed.")

    if result is None:
        raise HTTPException(status_code=400, detail="Failed to process the input.")

    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
