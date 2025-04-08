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

def test_inference_marker(start_api_app_docker) -> None:
    """
    Test PDF conversion using marker
    - Note: this may take 10s of seconds due to inference
    """
    response = requests.post("http://127.0.0.1:8080/marker/inference")
    assert response.status_code == 200
    assert response.json()['total_duration_in_second'] > 0
    assert response.json()['result'][0]['filename'] == 'ms-note-one-page.pdf'

def test_inference_sparrow(start_api_app_docker) -> None:
    """
    Test PDF conversion using sparrow
    """
    response = requests.post("http://127.0.0.1:8080/sparrow-ocr/inference")
    assert response.status_code == 200
    assert response.json()['total_duration_in_second'] > 0
    assert response.json()['result'][0]['filename'] == 'ms-note-one-page.pdf'