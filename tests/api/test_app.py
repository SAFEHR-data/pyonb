"""Test functions in /src/api/app/main.py."""

import os
from pathlib import Path

import pytest
import requests


@pytest.mark.usefixtures("local_start_api_app")
def test_local_start_api_and_healthy(ocr_forwarding_api_port: str) -> None:
    """Test API app comes up and healthcheck returns 200."""
    response = requests.get(f"http://127.0.0.1:{ocr_forwarding_api_port}/", timeout=5)
    assert response.status_code == requests.codes.ok
    assert response.url == f"http://127.0.0.1:{ocr_forwarding_api_port}/docs"


@pytest.mark.parametrize(
    "check_container_healthy",
    [
        "pyonb-ocr-forwarding-api-1",
        "pyonb-marker-1",
        "pyonb-sparrow-1",
        "pyonb-paddleocr-1",
    ],
    indirect=True,
)
def test_check_services(check_container_healthy: bool) -> None:
    """Test OCR API Docker services are up."""
    assert check_container_healthy, "Docker services not running. Required for full API testing."


def test_data_folder_contents() -> None:
    """
    Test documents data folder correct for testing.

    For testing, env variable HOST_DATA_FOLDER should mount /tests/data/single_synthetic_doc
    to CONTAINER_DATA_FOLDER, which should be /data inside the container.
    There should be a single test PDF file (ms-note-one-page.pdf) inside.
    """
    assert "single_synthetic_doc" in str(os.getenv("HOST_DATA_FOLDER")), (
        "For testing, HOST_DATA_FOLDER should point at /tests/data/single_synthetic_doc. "
        "Check environment variables if this fails. "
        f"HOST_DATA_FOLDER: {os.getenv('HOST_DATA_FOLDER')}"
    )
    assert "data" in str(os.getenv("CONTAINER_DATA_FOLDER")), (
        "CONTAINER_DATA_FOLDER should point at /data."
        "Check environment variables if this fails. "
        f"CONTAINER_DATA_FOLDER: {os.getenv('CONTAINER_DATA_FOLDER')}"
    )

    test_pdf_file_path = Path(str(os.getenv("HOST_DATA_FOLDER"))) / "ms-note-one-page.pdf"
    assert test_pdf_file_path.is_file(), f"File at {test_pdf_file_path} not found."
