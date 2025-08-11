"""Routers for Sparrow OCR."""

import datetime
import json
import logging
import os
from pathlib import Path
from typing import Annotated, Any

import requests
from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse

# Creating an object
logger = logging.getLogger()

# Detect if in Docker container
is_docker = Path("/.dockerenv").exists()

router = APIRouter()


def check_data_folder() -> Path | str:
    """Check if Docker or local deployment and adjust DATA_FOLDER accordingly."""
    # Detect if in Docker container
    is_docker = Path("/.dockerenv").exists()

    logger.info("HOST_DATA_FOLDER: %s", str(os.environ.get("HOST_DATA_FOLDER")))

    if is_docker:
        logger.info("Detected running inside Docker container.")
        DATA_FOLDER = str(os.environ.get("CONTAINER_DATA_FOLDER"))
    elif not is_docker:
        logger.info("Detected running on host machine.")
        DATA_FOLDER = str(os.environ.get("HOST_DATA_FOLDER"))

    if Path(DATA_FOLDER).exists():
        logger.info("DATA_FOLDER: %s", DATA_FOLDER)
    else:
        e = f"{Path(DATA_FOLDER)!s} not found or does not exist."
        logger.exception(NotADirectoryError(e))
        raise NotADirectoryError(e)

    return DATA_FOLDER


# nb: sparrow hard codes API port to 8001
@router.get("/sparrow-ocr")
async def healthcheck() -> dict[str, Any]:
    """Test aliveness endpoint for Sparrow."""
    logger.info("[GET] /sparrow")
    url = "http://sparrow:8001"
    response = requests.get(url, timeout=5)  # noqa: ASYNC210

    return json.loads(response.content.decode("utf-8"))


@router.post("/sparrow-ocr/inference_single", status_code=status.HTTP_200_OK)
async def inference_single_doc(file_upload: Annotated[UploadFile, File()] = None) -> JSONResponse:
    """
    Runs Sparrow OCR inference on a single document.

    UploadFile object forwarded onto inference API.
    """
    logger.info("[POST] /sparrow-ocr/inference_single_doc")
    url = "http://sparrow:8001/api/v1/sparrow-ocr/inference"  # fwd request to sparrow service

    t1 = datetime.datetime.now(datetime.UTC)

    file_bytes = await file_upload.read()
    file = {"file": (file_upload.filename, file_bytes, file_upload.content_type)}
    headers = {"accept": "application/json"}

    logger.info("post request - url: %s", url)
    logger.info("post request - file: %s", file)
    logger.info("post request - headers: %s", headers)

    # nb: timeout currently arbitrarily one hour
    response = requests.post(url=url, files=file, headers=headers, timeout=60 * 60)  # noqa: ASYNC210

    t2 = datetime.datetime.now(datetime.UTC)
    td = t2 - t1

    response_json = {
        "filename": str(file_upload.filename),
        "duration_in_second": td.total_seconds(),
        "ocr-result": response.json()['extracted_text'],
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_json)


@router.post("/sparrow-ocr/inference_folder")
async def inference_folder() -> dict:
    """Runs Sparrow OCR inference on multiple documents in a folder."""
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
