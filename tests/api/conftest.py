import subprocess
import time
import pytest

@pytest.fixture(scope="module")
def start_api_app():
    proc = subprocess.Popen(
        ["fastapi", "run", "main.py", "--host", "127.0.0.1", "--port", "8080"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(2)

    yield  # Yield control to tests

    proc.terminate()
    proc.wait()