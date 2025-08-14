"""PaddleOCR runner."""

import io
import itertools
import logging
import os
import time
from functools import lru_cache
from io import BytesIO
from pathlib import Path
from typing import Annotated, Any, NamedTuple

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from paddleocr import PaddleOCR, draw_ocr
from pdf2image import convert_from_bytes
from PIL.Image import Image
from starlette.responses import JSONResponse

# Creating an object
logger = logging.getLogger()

router = APIRouter()


class DocumentImage(NamedTuple):
    """Document Image Object for ocr processing."""

    doc: Image
    name: str
    content_type: str
    page_num: int


@lru_cache(maxsize=1)
def load_ocr_model(ocr_version: str, lang: str) -> PaddleOCR:
    """Load PaddleOCR official model with model version and Model Language."""
    return PaddleOCR(ocr_version=ocr_version, use_angle_cls=True, lang=lang, enable_mkldnn=True)


def merge_data(values: list[str]) -> list:
    """Flatten and merge the ocr text result."""
    data: list = []
    data.extend([values[idx][1][0]] for idx in range(len(values)))

    return data


def invoke_ocr(doc_image: DocumentImage, ocr_version: str, lang: str) -> tuple[list | list[Any], float]:
    """Process image and return ocr text and visualise ocr in jpeg."""
    worker_pid = os.getpid()
    logger.debug("Handling OCR request with worker PID: %d", worker_pid)
    start_time = time.time()

    model = load_ocr_model(ocr_version, lang)

    bytes_img = io.BytesIO()

    format_img = "JPEG"
    if doc_image.content_type == "image/png":
        format_img = "PNG"

    doc_image.doc.save(bytes_img, format=format_img)
    bytes_data = bytes_img.getvalue()

    result = model.ocr(bytes_data, cls=True)

    values, boxes, txts, scores = [], [], [], []
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

            image = Image.open(bytes_img).convert("RGB")
            im_show = draw_ocr(image, boxes, txts, scores, font_path="../fonts/DejaVuSerif.ttf")
            im_show = Image.fromarray(im_show)
            container_data_path = str(os.environ.get("CONTAINER_DATA_FOLDER"))
            output_dir_name = Path(container_data_path) / doc_image.name.split(".")[0]
            logger.debug("output_dir_name: %s", output_dir_name)
            # Create the directory
            try:
                Path(output_dir_name).mkdir()
                logger.info("Directory '%s' created successfully.", output_dir_name)
            except FileExistsError:
                logger.exception("Directory '%s' already exists.", output_dir_name)
            except PermissionError:
                logger.exception("Permission denied: Unable to create '%s'.")

            ocr_jpeg_file_name = doc_image.name + "_" + str(doc_image.page_num) + ".jpg"
            file_path = Path(output_dir_name) / ocr_jpeg_file_name
            im_show.save(file_path, "JPEG")

    bytes_img.close()
    end_time = time.time()
    processing_time = end_time - start_time
    logger.debug("OCR done, worker PID: %d", worker_pid)

    return values, processing_time


@router.post("/inference")
async def inference(
    file: Annotated[UploadFile, File()] = None,
    ocr_version: Annotated[str, Form()] = "PP-OCRv4",
    lang: Annotated[str, Form()] = "ch",
) -> JSONResponse:
    """Receive unprocessed files and call invoke_ocr page by page."""
    logger.info("ocr_version: %s ", ocr_version)
    logger.info("lang: %s", lang)
    total_proc_time, result = float(0), []
    logger.info("file.content_type: %s", file.content_type)
    if file:
        if file.content_type in ["image/jpeg", "image/jpg", "image/png"]:
            docs = Image.open(BytesIO(await file.read()))  # always 1 for image
        elif file.content_type == "application/pdf":
            pdf_bytes = await file.read()
            pages = convert_from_bytes(pdf_bytes, 300)
            docs = pages
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Invalid file type. Only JPG/PNG images and PDF are allowed."},
            )

        for page_num_counter, doc in enumerate(docs):
            logger.debug("file name: %s", file.filename)

            page_result, processing_time = invoke_ocr(
                doc_image=DocumentImage(
                    doc=doc, name=file.filename, content_type=file.content_type, page_num=page_num_counter
                ),
                ocr_version=ocr_version,
                lang=lang,
            )
            if page_result is not None:
                result.append(list(itertools.chain.from_iterable(page_result)))
            total_proc_time += processing_time

        logger.debug("Processing time OCR: {%f:.2f} seconds", total_proc_time)
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"info": "No input provided"})

    if result is None:
        raise HTTPException(status_code=400, detail="Failed to process the input.")

    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
