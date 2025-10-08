"""Test functions in /src/api/app/main.py."""

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
        "pyonb-paddleocr-1",
        "pyonb-docling-1",
        "pyonb-kreuzberg-1",
    ],
    indirect=True,
)
def test_check_services(check_container_healthy: bool) -> None:
    """Test OCR API Docker services are up."""
    assert check_container_healthy, "Docker services not running. Required for full API testing."
