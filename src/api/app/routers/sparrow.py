import json
import os

from fastapi import APIRouter
import datetime
import logging
import requests

logging.basicConfig(filename="sparrow-ocr." + datetime.datetime.now().strftime("%Y%m%d") + ".log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

router = APIRouter()

@router.get("/sparrow-ocr")
async def hello():
    logger.info("[GET] /sparrow")
    url= f"http://sparrow:8001"
    response = requests.get(url)

    return json.loads(response.content.decode('utf-8'))

@router.post("/sparrow-ocr/inference")
async def inference():
    logger.info("[POST] /sparrow-ocr/inference")
    url= f"http://sparrow:8001/api/v1/sparrow-ocr/inference" # fwd request to sparrow service, port 8001
    
    DATA_FOLDER = os.environ.get("CONTAINER_DATA_FOLDER")  # TODO: fix so env var can be on host or container
    logger.info(f"DATA_FOLDER: {DATA_FOLDER}")

    filenames = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".pdf")]
    logger.info(f"Filenames in {DATA_FOLDER}: {filenames}")

    ocr_result = []
    t1 = datetime.datetime.now()
    for filename in filenames:
        with open(os.path.join(DATA_FOLDER, filename), "rb") as pdf_file:
            # Send the file via POST request
            s1 = datetime.datetime.now()
            response = requests.post(url, files={"file": (filename , pdf_file, "application/pdf")})
            s2 = datetime.datetime.now()
            td = s2 - s1
            response_entry = {'filename': filename,
                              'duration_in_second': td.total_seconds() ,
                              'ocr-result': response.text}
            logger.info(f"Filename: {filename}")
            logger.info(f"response_entry: {response_entry}")
            ocr_result.append(response_entry)
    t2 = datetime.datetime.now()
    total_duration = t2 - t1
    response_json = {"total_duration_in_second" : total_duration.total_seconds(),
                     "result" : ocr_result}
    return response_json





