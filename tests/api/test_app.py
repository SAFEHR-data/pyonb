"""Test functions in /src/api/app/main.py."""

import pytest
import requests


@pytest.mark.usefixtures("start_api_app")
def test_start_api_and_healthy(ocr_api_port: str) -> None:
    """Test API app comes up and healthcheck returns 200."""
    response = requests.get(f"http://127.0.0.1:{ocr_api_port}/", timeout=5)
    assert response.status_code == requests.codes.ok
    assert response.json() == {"service": "pyonb-ocr-api", "status": "healthy"}


def test_start_api_and_healthy_docker(ocr_api_port: str) -> None:
    """Test API app comes up and healthcheck returns 200."""
    response = requests.get(f"http://127.0.0.1:{ocr_api_port}/", timeout=5)
    assert response.status_code == requests.codes.ok
    assert response.json() == {"service": "pyonb-ocr-api", "status": "healthy"}
