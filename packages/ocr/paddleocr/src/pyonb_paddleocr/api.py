"""PaddleOCR API."""

import datetime
import logging
import os
from functools import lru_cache
from typing import Annotated

import numpy as np
import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse, RedirectResponse
from paddleocr import PaddleOCR
from pdf2image import convert_from_bytes
from PIL import Image

PADDLEOCR_API_PORT = int(os.getenv("PADDLE_API_PORT", default="8114"))

_today = datetime.datetime.now(datetime.UTC).strftime("%Y_%m_%d")  # type: ignore[attr-defined] # mypy complains that 'Module has no attribute "UTC"'
logging.basicConfig(
    filename=f"paddleocr-{_today}.log",
    format="%(asctime)s %(message)s",
    filemode="a",
)

# Creating an object
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    """Redirect localhost:<PORT> to Swagger at localhost:<PORT>/docs."""
    return RedirectResponse(url="/docs")


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> JSONResponse:
    """
    Health check endpoint to verify API is accessible.

    Returns 200 OK status if API is running properly.
    """
    logger.info("[GET] /health")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"service": "paddleocr", "status": "healthy"},
    )


@lru_cache(maxsize=1)
def load_ocr_model(
    ocr_version: str,
    lang: str,
) -> PaddleOCR:
    """Load PaddleOCR official model with model version and Model Language."""
    return PaddleOCR(
        ocr_version=ocr_version,
        use_angle_cls=True,
        lang=lang,
        enable_mkldnn=True,
    )


def extract_text(pages: list[Image.Image], model: PaddleOCR) -> str:
    """Perform OCR to extract text from PDF pages using PaddleOCR."""
    all_text = ""
    for page in pages:
        results = model.ocr(np.array(page), cls=True)
        if results and results[0]:
            page_text = "\n".join([line[1][0] for line in results[0]])
            all_text += page_text + "\n"

    return all_text


@app.post("/inference", status_code=status.HTTP_200_OK)
async def inference(
    file: Annotated[UploadFile, File()] = None,
    ocr_version: Annotated[str, Form()] = "PP-OCRv4",
    lang: Annotated[str, Form()] = "en",
) -> JSONResponse:
    """
    Endpoint to execute paddleocr on PDF file.

    Returns 200 OK JSON formatted text result from paddleocr.
    """
    logger.info("[POST] /inference")
    logger.info("[POST] /inference - Received file: %s", file.filename)

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF are allowed.")

    model = load_ocr_model(
        ocr_version=ocr_version,
        lang=lang,
    )
    try:
        content = await file.read()
        pages = convert_from_bytes(content, 300)
        result = extract_text(
            pages=pages,
            model=model,
        )
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to run paddleocr. Error: {e}") from e


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=PADDLEOCR_API_PORT,
        reload=True,
        use_colors=True,
    )
