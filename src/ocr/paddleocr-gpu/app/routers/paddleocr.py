import io
import itertools
import logging
import os
import time
from functools import lru_cache
from io import BytesIO
from typing import Annotated

from PIL import Image
from fastapi import APIRouter
from fastapi import File, Form, HTTPException
from fastapi import status, UploadFile
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
from pdf2image import convert_from_bytes

# Creating an object
logger = logging.getLogger()

router = APIRouter()

@lru_cache(maxsize=1)
def load_ocr_model(ocr_model_version, ocr_model_lang):
    model = PaddleOCR(ocr_version=ocr_model_version, use_angle_cls=True, lang=ocr_model_lang, enable_mkldnn=True)
    return model

def merge_data(values):
    data = []
    for idx in range(len(values)):
        data.append([values[idx][1][0]])

    return data


def invoke_ocr(doc, content_type, ocr_model_version, ocr_model_lang):
    worker_pid = os.getpid()
    logger.debug(f"Handling OCR request with worker PID: {worker_pid}")
    start_time = time.time()

    model = load_ocr_model(ocr_model_version, ocr_model_lang)

    bytes_img = io.BytesIO()

    logger.debug(f"content_type: {content_type}")
    format_img = "JPEG"
    if content_type == "image/png":
        format_img = "PNG"

    doc.save(bytes_img, format=format_img)
    bytes_data = bytes_img.getvalue()
    bytes_img.close()

    result = model.ocr(bytes_data, cls=True)

    values = []
    for idx in range(len(result)):
        res = result[idx]
        if res is not None:
            for line in res:
                values.append(line)
            values = merge_data(values)

    end_time = time.time()
    processing_time = end_time - start_time
    logger.debug(f"OCR done, worker PID: {worker_pid}")

    return values, processing_time

@router.post("/inference")
async def inference(file: UploadFile = File(None),
                    ocr_model_version: Annotated[str, Form()] = "PP-OCRv4",
                    ocr_model_lang: Annotated[str, Form()] = "ch"):
    logger.info(f"ocr_model_version: {ocr_model_version}")
    logger.info(f"ocr_model_lang: {ocr_model_lang}")
    total_proc_time, total_page_size, result = 0 , 0, []

    if file:
        if file.content_type in ["image/jpeg", "image/jpg", "image/png"]:
            docs = Image.open(BytesIO(await file.read())) # always 1 for image
        elif file.content_type == "application/pdf":
            pdf_bytes = await file.read()
            pages = convert_from_bytes(pdf_bytes, 300)
            docs = pages
        else:
            return {"error": "Invalid file type. Only JPG/PNG images and PDF are allowed."}

        for doc in docs:
            logger.debug("file name: " + file.filename)
            page_result, processing_time = invoke_ocr(doc, file.content_type, ocr_model_version, ocr_model_lang)
            if page_result is not None:
                result.append(list(itertools.chain.from_iterable(page_result)))
            total_proc_time += processing_time

        logger.debug(f"Processing time OCR: {total_proc_time:.2f} seconds")
    else:
        result = {"info": "No input provided"}

    if result is None:
        raise HTTPException(status_code=400, detail=f"Failed to process the input.")

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"page_count": len(result) , "result" : result})