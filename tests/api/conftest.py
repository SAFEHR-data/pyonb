"""Testing setup."""

import json
import logging
import os
import subprocess
import time
from collections.abc import Generator

import pytest
from dotenv import load_dotenv

load_dotenv()


logging.basicConfig(
    format="%(asctime)s %(message)s",
    filemode="a",
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class StartApiError(Exception):
    """Raised when unable to start API."""

    def __init__(self) -> None:
        """Initialize the exception with a message."""
        super().__init__("Cannot find main.py to start API.")


def is_healthy(service: str) -> str | bool:
    """
    Checks if Docker service is healthy based.

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
    except (
        subprocess.CalledProcessError,
        KeyError,
        IndexError,
        json.JSONDecodeError,
    ) as e:
        logger.info("Error checking health for %s: %s", service, e)
        return False
    else:
        return health_status == "healthy"


def wait_for_service(docker_service_name: str, timeout: int = 180) -> bool:
    """
    Waits for Docker services to build and run.

    - if services are not up within the timeout duration, TimeoutError raised
    """
    logger.info("Waiting for %s to become healthy...", docker_service_name)
    start = time.time()
    while time.time() - start < timeout:
        if is_healthy(docker_service_name):
            logger.info("%s is healthy!", docker_service_name)
            return True
        time.sleep(20)
    e = f"{docker_service_name} did not become healthy in time."
    raise TimeoutError(e)


@pytest.fixture(scope="module")
def ocr_api_port() -> str | None:
    """Returns OCR_FORWARDING_API_PORT."""
    if os.getenv("OCR_FORWARDING_API_PORT"):
        return os.getenv("OCR_FORWARDING_API_PORT")
    e = "OCR_FORWARDING_API_PORT environment variable not found."
    raise NameError(e)


@pytest.fixture(scope="module")
def start_api_app() -> Generator:
    """
    Starts the forwarding API on the local host machine.

    - Note: does not start OCR tool APIs.
    """
    if not os.path.isfile("src/api/app/main.py"):
        StartApiError()

    proc = subprocess.Popen(
        [
            "fastapi",
            "run",
            "src/api/app/main.py",
            "--host",
            "127.0.0.1",
            "--port",
            str(os.environ.get("OCR_FORWARDING_API_PORT")),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    time.sleep(2)

    yield  # Yield control to tests

    proc.terminate()
    proc.wait()


@pytest.fixture(scope="module")
def start_api_app_docker() -> Generator:
    """Starts forwarding API and OCR tool APIs with Docker."""
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

    wait_for_service("pyonb-ocr-forwarding-api-1")  # TODO(tom): preferable not to hardcode service strings
    wait_for_service("pyonb-marker-1")
    wait_for_service("pyonb-sparrow-1")

    yield

    proc.terminate()
    proc.wait()
