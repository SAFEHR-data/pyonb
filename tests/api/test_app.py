"""Test functions in /src/api/app/main.py"""
import requests


def test_start_api_and_healthy(start_api_app) -> None:
    """Test API app comes up and healthcheck returns 200"""
    response = requests.get("http://127.0.0.1:8080/")
    assert response.status_code == 200
    assert response.json() == {"service":"pyonb-ocr-api", "status":"healthy"}
