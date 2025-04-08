import os
import subprocess
import time
import pytest

@pytest.fixture(scope="module")
def start_api_app():
    """
    Starts the forwarding API on the locally host machine
    - Note: does not start OCR tool APIs
    """
    if not os.path.isfile("src/api/app/main.py"):
        raise Exception("Cannot find main.py to start API.")
    
    proc = subprocess.Popen(
        ["fastapi", "run", "src/api/app/main.py", "--host", "127.0.0.1", "--port", "8080"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    time.sleep(2)

    yield  # Yield control to tests

    proc.terminate()
    proc.wait()

@pytest.fixture(scope="module")
def start_api_app_docker():
    """
    Starts forwarding API and OCR tool APIs with Docker
    """
    proc = subprocess.Popen(
        ["docker", "compose", 
         "--profile", "marker",
         "--profile", "sparrow",
         "up", "-d"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    time.sleep(2)

    yield

    proc.terminate()
    proc.wait()