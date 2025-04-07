import json
import os
import subprocess

from fastapi import APIRouter
import datetime
import logging
import requests

logging.basicConfig(filename="marker-ocr." + datetime.datetime.now().strftime("%Y%m%d") + ".log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Detect if in Docker container
is_docker = os.path.exists('/.dockerenv')

router = APIRouter()

@router.get("/marker/health")
async def health():
    logger.info("[GET] /marker/health")
    url = f"http://marker:8002/health"
    response = requests.get(url)

    return json.loads(response.content.decode('utf-8'))
