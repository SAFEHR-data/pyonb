"""Routers for Kreuzberg OCR."""

import aiohttp
import logging
import os
import time
from typing import Annotated, Any

from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse

# Creating an object
logger = logging.getLogger()

router = APIRouter()

KREUZBERG_API_PORT = os.getenv("KREUZBERG_API_PORT")


@router.get("/kreuzberg/health")
async def healthcheck() -> dict[str, Any]:
    """Test aliveness endpoint for Kreuzberg."""
    logger.info("[GET] /kreuzberg/health")
    url = f"http://kreuzberg:{KREUZBERG_API_PORT}/health"

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60 * 60)) as session:
            async with session.get(url) as response:
                response.raise_for_status()
    except aiohttp.ClientError as e:
        logger.exception(f"Failed to connect to kreuzberg service: {e}")
        raise

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"service": "kreuzberg", "status": "healthy"},
    )


@router.post("/kreuzberg-ocr/inference_single", status_code=status.HTTP_200_OK)
async def inference_single_doc(file_upload: Annotated[UploadFile, File()] = None) -> JSONResponse:
    """
    Runs Kreuzberg OCR inference on a single document.

    UploadFile object forwarded onto inference API.
    """
    logger.info("[POST] /kreuzberg-ocr/extract")
    url = f"http://kreuzberg:{KREUZBERG_API_PORT}/extract"  # fwd request to kreuzberg service

    data = aiohttp.FormData()
    data.add_field(
        "data",  # field name expected by Kreuzberg's /extract API
        file_upload.file,
        filename=file_upload.filename,
        content_type=file_upload.content_type,
    )
    headers = {"accept": "application/json"}

    logger.info("post request - url: %s", url)
    logger.info("post request - data: %s", data)
    logger.info("post request - headers: %s", headers)


    t1 = time.perf_counter()
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60 * 60)) as session:
            async with session.post(url, data=data, headers=headers) as response:
                response.raise_for_status()
                ocr_results = await response.json()
    except aiohttp.ClientError:
        logger.exception("Request Exception")
        raise
    t2 = time.perf_counter()

    # Kreuzberg's /extract API expects a list of documents and always returns a list of extracted text
    # We only ever extract and return content for a single document
    ocr_result = ocr_results[0]['content']

    response_json = {
        "filename": str(file_upload.filename),
        "duration_in_second": t2 - t1,
        "ocr-result": ocr_result,
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_json)
