"""Testing setup."""

import logging
from pathlib import Path

import pytest
from dotenv import load_dotenv

load_dotenv()


logging.basicConfig(
    format="%(asctime)s %(message)s",
    filemode="a",
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@pytest.fixture(scope="module")
def ground_truth_txt_filepath() -> Path:
    """
    Returns filepath of ground truth PDF (ms-note-one-page.pdf) transcription.

    Note: this is a simple copy-paste of the PDF into a .txt file.
    """
    return Path("tests/data/ocr_eval/copy_paste_ms-note-one-page.txt")

@pytest.fixture(scope="module")
def marker_ocr_json_filepath() -> Path:
    """Returns filepath of Marker OCR JSON output."""
    return Path("tests/data/ocr_eval/marker_ocr_ms-note-one-page.json")
