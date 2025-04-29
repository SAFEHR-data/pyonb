"""Routers for Marker OCR."""

import datetime
import json
import logging
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

load_dotenv()

if os.getenv("MARKER_API_PORT"):
    MARKER_API_PORT = os.getenv("MARKER_API_PORT")
else:
    e = "MARKER_API_PORT environment variable not found."
    raise NameError(e)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Detect if in Docker container
is_docker = Path("/.dockerenv").exists()

router = APIRouter()


@router.get("/marker/health")
async def health() -> dict[str, Any]:
    """Test aliveness endpoint for Marker."""
    logger.info("[GET] /marker/health")
    url = f"http://marker:{MARKER_API_PORT}/health"
    response = requests.get(url, timeout=5)  # noqa: ASYNC210

    return json.loads(response.content.decode("utf-8"))


@router.post("/marker/inference")
async def inference() -> JSONResponse:
    """Runs Marker OCR inference."""
    logger.info("[POST] /marker/inference")
    url = f"http://marker:{MARKER_API_PORT}/inference"
    # URL of marker service
    # TODO(tom): configure with env var (e.g. so can set 127.0.0.1 if running on host)

    if is_docker:
        logger.info("Detected running inside Docker container.")
        DATA_FOLDER = str(os.environ.get("CONTAINER_DATA_FOLDER"))
    elif not is_docker:
        logger.info("Detected running on host machine.")
        DATA_FOLDER = str(os.environ.get("HOST_DATA_FOLDER"))
    logger.info("DATA_FOLDER: %s", DATA_FOLDER)

    filenames = [f for f in Path(DATA_FOLDER).iterdir() if f.suffix == ".pdf"]
    logger.info("Filenames in %s: %s", DATA_FOLDER, filenames)

    ocr_result = []
    t1 = datetime.datetime.now(datetime.UTC)
    for filename in filenames:
        with Path.open(Path(str(DATA_FOLDER)) / Path(str(filename)), "rb") as pdf_file:
            # Send the file via POST request
            s1 = datetime.datetime.now(datetime.UTC)

            files = {"file": (str(filename), pdf_file, "application/pdf")}
            headers = {"accept": "application/json"}
            response = requests.post(url, files=files, headers=headers, timeout=5)  # noqa: ASYNC210

            s2 = datetime.datetime.now(datetime.UTC)
            td = s2 - s1
            response_entry = {
                "filename": filename,
                "duration_in_second": td.total_seconds(),
                "ocr-result": response.text,
            }
            logger.info("Filename: %s", filename)
            logger.info("response_entry: %s", response_entry)
            ocr_result.append(response_entry)

    t2 = datetime.datetime.now(datetime.UTC)
    total_duration = t2 - t1
    response_json = {
        "total_duration_in_second": total_duration.total_seconds(),
        "result": ocr_result,
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_json)
