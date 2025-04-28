import datetime
import json
import logging
import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

load_dotenv()

if os.getenv("MARKER_API_PORT"):
    MARKER_API_PORT = os.getenv("MARKER_API_PORT")
else:
    raise NameError("MARKER_API_PORT environment variable not found.")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Detect if in Docker container
is_docker = os.path.exists("/.dockerenv")

router = APIRouter()


@router.get("/marker/health")
async def health():
    logger.info("[GET] /marker/health")
    url = f"http://marker:{MARKER_API_PORT}/health"
    response = requests.get(url)

    return json.loads(response.content.decode("utf-8"))


@router.post("/marker/inference")
async def inference():
    logger.info("[POST] /marker/inference")
    url = f"http://marker:{MARKER_API_PORT}/inference"  # URL of marker service - TODO: configure with env var (e.g. so can set 127.0.0.1 if running on host)

    if is_docker:
        logger.info("Detected running inside Docker container.")
        DATA_FOLDER = os.environ.get("CONTAINER_DATA_FOLDER")
    elif not is_docker:
        logger.info("Detected running on host machine.")
        DATA_FOLDER = os.environ.get("HOST_DATA_FOLDER")
    logger.info(f"DATA_FOLDER: {DATA_FOLDER}")

    filenames = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".pdf")]
    logger.info(f"Filenames in {DATA_FOLDER}: {filenames}")

    ocr_result = []
    t1 = datetime.datetime.now()
    for filename in filenames:
        with open(os.path.join(DATA_FOLDER, filename), "rb") as pdf_file:
            # Send the file via POST request
            s1 = datetime.datetime.now()

            files = {"file": (filename, pdf_file, "application/pdf")}
            headers = {"accept": "application/json"}
            response = requests.post(url, files=files, headers=headers)

            s2 = datetime.datetime.now()
            td = s2 - s1
            response_entry = {
                "filename": filename,
                "duration_in_second": td.total_seconds(),
                "ocr-result": response.text,
            }
            logger.info(f"Filename: {filename}")
            logger.info(f"response_entry: {response_entry}")
            ocr_result.append(response_entry)
    t2 = datetime.datetime.now()
    total_duration = t2 - t1
    response_json = {
        "total_duration_in_second": total_duration.total_seconds(),
        "result": ocr_result,
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_json)
