"""Test functions in /src/api/app/routers"""
import requests


def test_router_marker(start_api_app_docker) -> None:
    """
    Test router for marker
    """
    response = requests.get("http://127.0.0.1:8080/marker/health")
    assert response.status_code == 200
    assert response.json() == {"service":"marker", "status":"healthy"}

def test_router_sparrow(start_api_app_docker) -> None:
    """
    Test router for sparrow
    - Note: uses sparrow devs' own API
    """
    response = requests.get("http://127.0.0.1:8080/sparrow-ocr")
    assert response.status_code == 200
    assert response.json() == {"message":"Sparrow OCR API"}
