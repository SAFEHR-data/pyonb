import json
import os
import subprocess
import time

import pytest
from dotenv import load_dotenv

load_dotenv()


def is_healthy(service):
    """
    Checks if Docker service is healthy based
    - Returns True if docker inspect <service> returns "healthy" status
    """
    try:
        result = subprocess.run(
            ["docker", "inspect", service],
            capture_output=True,
            text=True,
            check=True,  # raises CalledProcessError if container not found
        )
        inspect_data = json.loads(result.stdout)
        health_status = inspect_data[0]["State"]["Health"]["Status"]
        return health_status == "healthy"
    except (
        subprocess.CalledProcessError,
        KeyError,
        IndexError,
        json.JSONDecodeError,
    ) as e:
        print(f"Error checking health for {service}: {e}")
        return False


def wait_for_service(docker_service_name, timeout=180):
    """
    Waits for Docker services to build and run
    - if services are not up within the timeout duration, TimeoutError raised
    """
    print(f"Waiting for {docker_service_name} to become healthy...")
    start = time.time()
    while time.time() - start < timeout:
        if is_healthy(docker_service_name):
            print(f"{docker_service_name} is healthy!")
            return True
        time.sleep(20)
    raise TimeoutError(f"{docker_service_name} did not become healthy in time.")


@pytest.fixture
def ocr_api_port(scope="module"):
    if os.getenv("OCR_FORWARDING_API_PORT"):
        return os.getenv("OCR_FORWARDING_API_PORT")
    raise NameError("OCR_FORWARDING_API_PORT environment variable not found.")


@pytest.fixture(scope="module")
def start_api_app():
    """
    Starts the forwarding API on the locally host machine
    - Note: does not start OCR tool APIs
    """
    if not os.path.isfile("src/api/app/main.py"):
        raise Exception("Cannot find main.py to start API.")

    proc = subprocess.Popen(
        [
            "fastapi",
            "run",
            "src/api/app/main.py",
            "--host",
            "127.0.0.1",
            "--port",
            os.environ.get("OCR_FORWARDING_API_PORT"),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
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
        [
            "docker",
            "compose",
            "--profile",
            "marker",
            "--profile",
            "sparrow",
            "up",
            "-d",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    time.sleep(2)

    wait_for_service("pyonb-ocr-forwarding-api-1")  # TODO preferable not to hardcode service strings
    wait_for_service("pyonb-marker-1")
    wait_for_service("pyonb-sparrow-1")

    yield

    proc.terminate()
    proc.wait()
