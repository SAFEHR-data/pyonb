import json
import os

from fastapi import APIRouter, HTTPException
import datetime
import logging
import requests

# Creating an object
logger = logging.getLogger()

# Detect if in Docker container
is_docker = os.path.exists('/.dockerenv')

router = APIRouter()

@router.get("/paddleocr")
async def health():
    logger.info("[GET] /paddleocr")
    url= f"http://paddleocr:8000/health"

    try:
        response = requests.get(url)
        return json.loads(response.content.decode('utf-8'))
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=repr(e))

def inference(url, ocr_version: str = None, lang: str = None):
    if is_docker:
        logger.info(f"Detected running inside Docker container.")
        DATA_FOLDER = os.environ.get("CONTAINER_DATA_FOLDER")
    elif not is_docker:
        logger.info(f"Detected running on host machine.")
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
            try:
                response = requests.post(url,
                                         files={"file": (filename , pdf_file, "application/pdf")},
                                         data={"ocr_version": ocr_version, "lang": lang })
            except Exception as e:
                logger.error(e, exc_info=True)
                raise HTTPException(status_code=500, detail=repr(e))

            s2 = datetime.datetime.now()
            td = s2 - s1
            response_entry = {'filename': filename,
                              'duration_in_second': td.total_seconds(),
                              'ocr-result': json.loads(response.content.decode('utf-8'))}
            logger.info(f"Filename: {filename}")
            logger.info(f"response_entry: {response_entry}")
            ocr_result.append(response_entry)
    t2 = datetime.datetime.now()
    total_duration = t2 - t1
    response_json = {"total_duration_in_second" : total_duration.total_seconds(),
                     "result" : ocr_result}
    return response_json


@router.post("/paddleocr/inference")
async def inference(model_version: str = None, model_lang: str = None):
    logger.info("[POST] /paddleocr/inference")
    logger.debug("model_version :" + str(model_version))
    logger.debug("model_lang" + str(model_lang))

    url= f"http://paddleocr:8000/inference"

    return inference(url, model_version, model_lang)








