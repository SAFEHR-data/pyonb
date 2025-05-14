"""Testing setup."""

import json
import logging
import os
import subprocess
import time
from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
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


@pytest.fixture(scope="module")
def check_container_healthy(request: SubRequest) -> str | bool:
    """
    Checks if Docker service is healthy based on docker inspect health status.

    - Returns True if docker inspect <service> returns "healthy" status
    """
    service = request.param
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


@pytest.fixture(scope="module")
def ocr_forwarding_api_port() -> str | None:
    """Returns OCR_FORWARDING_API_PORT."""
    if os.getenv("OCR_FORWARDING_API_PORT"):
        return os.getenv("OCR_FORWARDING_API_PORT")
    e = "OCR_FORWARDING_API_PORT environment variable not found."
    raise NameError(e)


@pytest.fixture(scope="module")
def local_start_api_app() -> Generator:
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
