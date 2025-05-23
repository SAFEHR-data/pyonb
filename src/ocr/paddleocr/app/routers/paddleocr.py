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
from paddleocr import PaddleOCR, draw_ocr
from pdf2image import convert_from_bytes

# Creating an object
logger = logging.getLogger()

router = APIRouter()

@lru_cache(maxsize=1)
def load_ocr_model(ocr_version, lang):
    model = PaddleOCR(ocr_version=ocr_version, use_angle_cls=True, lang=lang, enable_mkldnn=True)
    return model

def merge_data(values):
    data = []
    for idx in range(len(values)):
        data.append([values[idx][1][0]])

    return data


def invoke_ocr(doc, file_name, file_content_type, page_num, ocr_version, lang):
    worker_pid = os.getpid()
    logger.debug(f"Handling OCR request with worker PID: {worker_pid}")
    start_time = time.time()

    model = load_ocr_model(ocr_version, lang)

    bytes_img = io.BytesIO()

    format_img = "JPEG"
    if file_content_type == "image/png":
        format_img = "PNG"

    doc.save(bytes_img, format=format_img)
    bytes_data = bytes_img.getvalue()

    result = model.ocr(bytes_data, cls=True)

    values, boxes, txts, scores = [],[],[],[]
    logger.debug(result)
    for idx in range(len(result)):
        res = result[idx]
        if res is not None:
            for line in res:
                values.append(line)
                boxes.append(line[0])
                txts.append(line[1][0])
                scores.append(line[1][1])
            values = merge_data(values)
            # draw result
            from PIL import Image
            image = Image.open(bytes_img).convert('RGB')
            im_show = draw_ocr(image, boxes, txts, scores,
                               font_path="/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
            im_show = Image.fromarray(im_show)
            output_dir_name = os.path.join(os.environ.get("CONTAINER_DATA_FOLDER"), file_name.split('.')[0])
            print("output_dir_name:" + output_dir_name)
            # Create the directory
            try:
                os.mkdir(output_dir_name)
                print(f"Directory '{output_dir_name}' created successfully.")
            except FileExistsError:
                print(f"Directory '{output_dir_name}' already exists.")
            except PermissionError:
                print(f"Permission denied: Unable to create '{output_dir_name}'.")
            except Exception as e:
                print(f"An error occurred: {e}")
            file_path = os.path.join(output_dir_name,file_name +"_" + str(page_num) + ".jpg")
            im_show.save(file_path, "JPEG")

    bytes_img.close()
    end_time = time.time()
    processing_time = end_time - start_time
    logger.debug(f"OCR done, worker PID: {worker_pid}")

    return values, processing_time

@router.post("/inference")
async def inference(file: UploadFile = File(None),
                    ocr_version: Annotated[str, Form()] = "PP-OCRv4",
                    lang: Annotated[str, Form()] = "ch"):
    logger.info(f"ocr_version: {ocr_version}")
    logger.info(f"lang: {lang}")
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

        for page_num_counter, doc in enumerate(docs):
            logger.debug("file name: " + file.filename)
            page_result, processing_time = invoke_ocr(doc=doc, file_name=file.filename, file_content_type=file.content_type,
                                                      page_num=page_num_counter,
                                                      ocr_version=ocr_version, lang=lang)
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