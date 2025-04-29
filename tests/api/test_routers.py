"""Test functions in /src/api/app/routers."""

import pytest
import requests


@pytest.mark.usefixtures("start_api_app_docker")
def test_router_marker(ocr_api_port: str) -> None:
    """Test router for marker."""
    response = requests.get(f"http://127.0.0.1:{ocr_api_port}/marker/health", timeout=5)
    assert response.status_code == requests.codes.ok
    assert response.json() == {"service": "marker", "status": "healthy"}


@pytest.mark.usefixtures("start_api_app_docker")
def test_router_sparrow(ocr_api_port: str) -> None:
    """
    Test router for sparrow.

    - Note: uses sparrow devs' own API.
    """
    response = requests.get(f"http://127.0.0.1:{ocr_api_port}/sparrow-ocr", timeout=5)
    assert response.status_code == requests.codes.ok
    assert response.json() == {"message": "Sparrow OCR API"}


@pytest.mark.usefixtures("start_api_app_docker")
def test_inference_marker(ocr_api_port: str) -> None:
    """
    Test PDF conversion using marker.

    - Note: this may take 10s of seconds due to inference
    """
    response = requests.post(f"http://127.0.0.1:{ocr_api_port}/marker/inference", timeout=5)
    assert response.status_code == requests.codes.ok
    assert response.json()["total_duration_in_second"] > 0
    assert response.json()["result"][0]["filename"] == "ms-note-one-page.pdf"


@pytest.mark.usefixtures("start_api_app_docker")
def test_inference_sparrow(ocr_api_port: str) -> None:
    """Test PDF conversion using sparrow."""
    response = requests.post(f"http://127.0.0.1:{ocr_api_port}/sparrow-ocr/inference", timeout=5)
    assert response.status_code == requests.codes.ok
    assert response.json()["total_duration_in_second"] > 0
    assert response.json()["result"][0]["filename"] == "ms-note-one-page.pdf"
