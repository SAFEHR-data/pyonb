"""
Test functions in /src/api/app/routers.

- Note: Tests require running Docker services.
"""

from pathlib import Path

import requests


def test_router_marker(ocr_forwarding_api_port: str) -> None:
    """Test healthcheck for marker."""
    response = requests.get(f"http://127.0.0.1:{ocr_forwarding_api_port}/marker/health", timeout=5)
    assert response.status_code == requests.codes.ok
    assert response.json() == {"service": "marker", "status": "healthy"}


def test_router_sparrow(ocr_forwarding_api_port: str) -> None:
    """
    Test healthcheck for sparrow.

    - Note: uses sparrow devs' own API.
    """
    response = requests.get(f"http://127.0.0.1:{ocr_forwarding_api_port}/sparrow-ocr", timeout=5)
    assert response.status_code == requests.codes.ok
    assert response.json() == {"message": "Sparrow OCR API"}


def test_router_paddleocr(ocr_forwarding_api_port: str) -> None:
    """Test healthcheck for marker."""
    response = requests.get(f"http://127.0.0.1:{ocr_forwarding_api_port}/paddleocr/health", timeout=5)
    assert response.status_code == requests.codes.ok
    assert response.json() == {"service": "paddleocr", "status": "healthy"}


def test_inference_marker(ocr_forwarding_api_port: str) -> None:
    """
    Test PDF conversion using marker.

    Note:
    - may take ~minutes to perform inference
    - four possible files assertion depending on whether testing single_synthetic_doc or multiple_synthetic_docs folder

    """
    response = requests.post(f"http://127.0.0.1:{ocr_forwarding_api_port}/marker/inference", timeout=60 * 60)
    assert response.status_code == requests.codes.ok
    assert response.json()["total_duration_in_second"] > 0
    assert response.json()["result"][0]["filename"] in {
        "ms-note-one-page.pdf",
        "uk-hospital-note.pdf",
        "uk-hospital-note-2.pdf",
        "uk-hospital-note-3.pdf",
    }


def test_inference_sparrow(ocr_forwarding_api_port: str) -> None:
    """
    Test PDF conversion using sparrow.

    Note:
    - may take ~minutes to perform inference
    - four possible files assertion depending on whether testing single_synthetic_doc or multiple_synthetic_docs folder

    """
    response = requests.post(f"http://127.0.0.1:{ocr_forwarding_api_port}/sparrow-ocr/inference", timeout=60 * 60)
    assert response.status_code == requests.codes.ok
    assert response.json()["total_duration_in_second"] > 0
    assert response.json()["result"][0]["filename"] in {
        "ms-note-one-page.pdf",
        "uk-hospital-note.pdf",
        "uk-hospital-note-2.pdf",
        "uk-hospital-note-3.pdf",
    }


def test_inference_single_file_upload_paddleocr(ocr_forwarding_api_port: str, single_pdf_filepath: Path) -> None:
    """Test PDF conversion using marker with single file endpoint."""
    url = f"http://127.0.0.1:{ocr_forwarding_api_port}/paddleocr/inference_single"

    single_pdf_filename = single_pdf_filepath.name

    with Path.open(single_pdf_filepath, "rb") as f:
        files = {"file_upload": (single_pdf_filename, f, "application/pdf")}
        response = requests.post(url, files=files, timeout=60 * 60)

    assert response.status_code == requests.codes.ok
    assert response.json()["duration_in_second"] > 0
    assert response.json()["filename"] in single_pdf_filename


def test_inference_on_folder_paddleocr(ocr_forwarding_api_port: str) -> None:
    """
    Test PDF conversion using Docling pointed at a folder of files.

    Note:
    - may take ~minutes to perform inference
    - four possible files assertion depending on whether testing single_synthetic_doc or multiple_synthetic_docs folder

    """
    response = requests.post(f"http://127.0.0.1:{ocr_forwarding_api_port}/paddleocr/inference_folder", timeout=60 * 60)
    assert response.status_code == requests.codes.ok
    assert response.json()["total_duration_in_second"] > 0
    assert response.json()["result"][0]["filename"] in {
        "ms-note-one-page.pdf",
        "uk-hospital-note.pdf",
        "uk-hospital-note-2.pdf",
        "uk-hospital-note-3.pdf",
    }
