"""Routers for Sparrow OCR."""

import datetime
import json
import logging
from pathlib import Path
from typing import Any

import requests
from fastapi import APIRouter

from api.app.util import check_data_folder

# Creating an object
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Detect if in Docker container
is_docker = Path("/.dockerenv").exists()

router = APIRouter()


# nb: sparrow hard codes API port to 8001
@router.get("/sparrow-ocr")
async def hello() -> dict[str, Any]:
    """Test aliveness endpoint for Sparrow."""
    logger.info("[GET] /sparrow")
    url = "http://sparrow:8001"
    response = requests.get(url, timeout=5)  # noqa: ASYNC210

    return json.loads(response.content.decode("utf-8"))


@router.post("/sparrow-ocr/inference")
async def inference() -> dict:
    """Runs Sparrow OCR inference."""
    logger.info("[POST] /sparrow-ocr/inference")
    url = "http://sparrow:8001/api/v1/sparrow-ocr/inference"  # fwd request to sparrow service

    DATA_FOLDER = check_data_folder()

    filenames = [str(f.name) for f in Path(DATA_FOLDER).iterdir() if f.suffix == ".pdf"]
    logger.info("Filenames in %s: %s", DATA_FOLDER, filenames)

    ocr_result = []
    t1 = datetime.datetime.now(datetime.UTC)
    for filename in filenames:
        abs_file_path = Path(DATA_FOLDER) / Path(filename)
        logger.info("abs_file_path: %s", abs_file_path)
        if not abs_file_path.exists():
            e = f"{abs_file_path!s} file not found or does not exist."
            logger.exception(FileNotFoundError(e))
            raise FileNotFoundError(e)

        with Path.open(abs_file_path, "rb") as pdf_file:
            # Send the file via POST request
            s1 = datetime.datetime.now(datetime.UTC)

            files = {"file": (str(filename), pdf_file, "application/pdf")}
            headers = {"accept": "application/json"}

            logger.info("post request - url: %s", url)
            logger.info("post request - files: %s", files)
            logger.info("post request - headers: %s", headers)

            # nb: timeout currently arbitrarily one hour
            response = requests.post(url, files=files, headers=headers, timeout=60 * 60)  # noqa: ASYNC210

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

    return {
        "total_duration_in_second": total_duration.total_seconds(),
        "result": ocr_result,
    }
