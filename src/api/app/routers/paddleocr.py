"""Routers for Paddle OCR."""

import json
import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Any

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

load_dotenv()

if os.getenv("PADDLEOCR_API_PORT"):
    PADDLEOCR_API_PORT = os.getenv("PADDLEOCR_API_PORT")
else:
    e = "PADDLEOCR_API_PORT environment variable not found."
    raise NameError(e)

# Creating an object
logger = logging.getLogger()

# Detect if in Docker container
is_docker = Path("/.dockerenv").exists()

router = APIRouter()


@router.get("/paddleocr/health")
async def health_check() -> dict[str, Any]:
    """
    Health check endpoint to verify API is accessible.

    Returns 200 OK status if API is running properly.
    """
    logger.info("[GET] /paddleocr/health")
    url = f"http://paddleocr:{PADDLEOCR_API_PORT}/health"

    try:
        response = requests.get(url, timeout=5)  # noqa: ASYNC210
        return json.loads(response.content.decode("utf-8"))
    except Exception as e:
        logger.exception("Connection exception when calling paddleocr")
        raise HTTPException(status_code=500, detail=repr(e)) from e


@router.post("/paddleocr/inference_single", status_code=status.HTTP_200_OK)
async def inference_single_doc(
    file_upload: Annotated[UploadFile, File()] = None,
    ocr_model_version: Annotated[str | None, Form()] = None,
    ocr_model_lang: Annotated[str | None, Form()] = None,
) -> JSONResponse:
    """
    Runs Paddle OCR inference on a single document.

    UploadFile object forwarded onto inference API.
    """
    logger.info("[POST] /paddleocr/inference_single_doc")
    url = f"http://paddleocr:{PADDLEOCR_API_PORT}/inference"

    t1 = datetime.now(tz=UTC)

    file_bytes = await file_upload.read()
    file = {"file": (file_upload.filename, file_bytes, file_upload.content_type)}

    logger.info("post request - url: %s", url)
    logger.info("post request - file: %s", file)

    # nb: timeout currently arbitrarily one hour
    data = {"model_version": ocr_model_version, "model_lang": ocr_model_lang}
    response = requests.post(url=url, files=file, data=data, timeout=60 * 60)  # noqa: ASYNC210

    t2 = datetime.now(tz=UTC)
    td = t2 - t1

    response_json = {
        "filename": str(file_upload.filename),
        "duration_in_second": td.total_seconds(),
        "ocr-result": response.json(),
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_json)


@router.post("/paddleocr/inference_folder")
async def inference_folder(model_version: str | None = None, model_lang: str | None = None) -> dict[str, Any]:
    """Runs PaddleOCR inference on multiple documents in a folder."""
    logger.info("[POST] /paddleocr/inference")
    logger.debug("model_version : %s", str(model_version))
    logger.debug("model_lang : %s", str(model_lang))
    url = f"http://paddleocr:{PADDLEOCR_API_PORT}/inference"

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

    filenames = [str(f.name) for f in Path(DATA_FOLDER).iterdir() if f.suffix == ".pdf"]
    logger.info("Filenames in %s: %s", DATA_FOLDER, filenames)

    ocr_result = []
    t1 = datetime.now(tz=UTC)
    for filename in filenames:
        abs_file_path = Path(DATA_FOLDER) / Path(filename)
        logger.info("abs_file_path: %s", abs_file_path)
        if not abs_file_path.exists():
            e = f"{abs_file_path!s} file not found or does not exist."
            logger.exception(FileNotFoundError(e))
            raise FileNotFoundError(e)

        with Path.open(abs_file_path, "rb") as pdf_file:
            # Send the file via POST request
            s1 = datetime.now(tz=UTC)
            files = {"file": (str(filename), pdf_file, "application/pdf")}
            data = {"model_version": model_version, "model_lang": model_lang}
            response = requests.post(url, files=files, data=data, timeout=60 * 60)  # noqa: ASYNC210

            s2 = datetime.now(tz=UTC)
            td = s2 - s1
            response_entry = {
                "filename": filename,
                "duration_in_second": td.total_seconds(),
                "ocr-result": json.loads(response.content.decode("utf-8")),
            }
            logger.info("Filename: %s", filename)
            logger.info("response_entry: %s", response_entry)
            ocr_result.append(response_entry)
    t2 = datetime.now(tz=UTC)
    total_duration = t2 - t1

    return {"total_duration_in_second": total_duration.total_seconds(), "result": ocr_result}
