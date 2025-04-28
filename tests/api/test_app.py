"""Test functions in /src/api/app/main.py"""

import requests


def test_start_api_and_healthy(start_api_app, ocr_api_port) -> None:
    """Test API app comes up and healthcheck returns 200"""
    response = requests.get(f"http://127.0.0.1:{ocr_api_port}/")
    assert response.status_code == 200
    assert response.json() == {"service": "pyonb-ocr-api", "status": "healthy"}


def test_start_api_and_healthy_docker(start_api_app_docker, ocr_api_port) -> None:
    """Test API app comes up and healthcheck returns 200"""
    response = requests.get(f"http://127.0.0.1:{ocr_api_port}/")
    assert response.status_code == 200
    assert response.json() == {"service": "pyonb-ocr-api", "status": "healthy"}
