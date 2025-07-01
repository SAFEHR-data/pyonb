"""Routers for Docling OCR."""

import datetime
import json
import logging
import os
from pathlib import Path
from typing import Annotated, Any

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse

load_dotenv()

if os.getenv("DOCLING_API_PORT"):
    DOCLING_API_PORT = os.getenv("DOCLING_API_PORT")
else:
    e = "DOCLING_API_PORT environment variable not found."
    raise NameError(e)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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


@router.get("/docling/health")
async def health() -> dict[str, Any]:
    """Test aliveness endpoint for Docling."""
    logger.info("[GET] /docling/health")
    url = f"http://docling:{DOCLING_API_PORT}/health"
    response = requests.get(url, timeout=5)  # noqa: ASYNC210

    return json.loads(response.content.decode("utf-8"))


@router.post("/docling/inference_single", status_code=status.HTTP_200_OK)
async def inference_single_doc(file_upload: Annotated[UploadFile, File()] = None) -> JSONResponse:
    """
    Runs Docling OCR inference on a single document.

    UploadFile object forwarded onto inference API.
    """
    logger.info("[POST] /docling/inference_single_doc")
    url = f"http://docling:{DOCLING_API_PORT}/inference"

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
        "ocr-result": json.loads(response.text),
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_json)


@router.post("/docling/inference_folder")
async def inference_folder() -> JSONResponse:
    """Runs Docling OCR inference on multiple documents in a folder."""
    logger.info("[POST] /docling/inference_folder")
    url = f"http://docling:{DOCLING_API_PORT}/inference"
    # URL of docling service
    # TODO(tom): configure with env var (e.g. so can set 127.0.0.1 if running on host)

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
    response_json = {
        "total_duration_in_second": total_duration.total_seconds(),
        "result": ocr_result,
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_json)
