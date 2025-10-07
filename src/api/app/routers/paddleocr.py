"""Routers for Paddle OCR."""

import logging
import os
import time
from pathlib import Path
from typing import Annotated, Any

import aiohttp
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

router = APIRouter()


@router.get("/paddleocr/health")
async def health_check() -> dict[str, Any]:
    """Test aliveness endpoint for Docling."""
    logger.info("[GET] /paddleocr/health")
    url = f"http://paddleocr:{PADDLEOCR_API_PORT}/health"

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60 * 60)) as session:  # noqa: SIM117
            async with session.get(url) as response:
                response.raise_for_status()
    except aiohttp.ClientError:
        logger.exception("Failed to connect to paddleocr service")
        raise

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"service": "paddleocr", "status": "healthy"},
    )


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

    data = aiohttp.FormData()
    data.add_field(
        "file",
        file_upload.file,
        filename=file_upload.filename,
        content_type=file_upload.content_type,
    )
    if ocr_model_version:
        data.add_field("ocr_version", ocr_model_version)
    if ocr_model_lang:
        data.add_field("lang", ocr_model_lang)
    headers = {"accept": "application/json"}

    logger.info("post request - url: %s", url)
    logger.info("post request - file: %s", data)
    logger.info("post request - headers: %s", headers)

    t1 = time.perf_counter()
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60 * 60)) as session:  # noqa: SIM117
            async with session.post(url, data=data, headers=headers) as response:
                response.raise_for_status()
                ocr_result = await response.json()
    except aiohttp.ClientError:
        logger.exception("Request Exception")
        raise
    t2 = time.perf_counter()

    response_json = {
        "filename": str(file_upload.filename),
        "duration_in_second": t2 - t1,
        "ocr-result": ocr_result,
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_json)


@router.post("/paddleocr/inference_folder")
async def inference_folder(model_version: str | None = None, model_lang: str | None = None) -> dict[str, Any]:
    """Runs PaddleOCR inference on multiple documents in a folder."""
    logger.info("[POST] /paddleocr/inference_folder")
    logger.debug("model_version : %s", str(model_version))
    logger.debug("model_lang : %s", str(model_lang))
    url = f"http://paddleocr:{PADDLEOCR_API_PORT}/inference"

    DATA_FOLDER = os.environ.get("DATA_FOLDER")
    if DATA_FOLDER is None:
        raise HTTPException(
            status_code=500,
            detail="DATA_FOLDER environment variable not defined.",
        )

    filenames = [str(f.name) for f in Path(DATA_FOLDER).iterdir() if f.suffix == ".pdf"]
    logger.info("Filenames in %s: %s", DATA_FOLDER, filenames)

    ocr_result = []
    t1 = time.perf_counter()
    for filename in filenames:
        abs_file_path = Path(DATA_FOLDER) / Path(filename)
        logger.info("abs_file_path: %s", abs_file_path)
        if not abs_file_path.exists():
            e = f"{abs_file_path!s} file not found or does not exist."
            logger.exception(FileNotFoundError(e))
            raise FileNotFoundError(e)

        with Path.open(abs_file_path, "rb") as pdf_file:
            # Send the file via POST request
            s1 = time.perf_counter()

            files = {"file": (str(filename), pdf_file, "application/pdf")}
            data = {"model_version": model_version, "model_lang": model_lang}
            headers = {"accept": "application/json"}

            logger.info("post request - url: %s", url)
            logger.info("post request - files: %s", files)
            logger.info("post request - headers: %s", headers)

            # nb: timeout currently arbitrarily one hour
            response = requests.post(url, files=files, data=data, headers=headers, timeout=60 * 60)  # noqa: ASYNC210

            s2 = time.perf_counter()
            response_entry = {
                "filename": filename,
                "duration_in_second": s2 - s1,
                "ocr-result": response.text,
            }
            logger.info("Filename: %s", filename)
            logger.info("response_entry: %s", response_entry)
            ocr_result.append(response_entry)

    t2 = time.perf_counter()
    response_json = {
        "total_duration_in_second": t2 - t1,
        "result": ocr_result,
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_json)
