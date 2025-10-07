"""Utility functions for OCR API."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def check_data_folder() -> Path | str:
    """Check if Docker or local deployment and adjust DATA_FOLDER accordingly."""
    # Detect if in Docker container
    is_docker = Path("/.dockerenv").exists()

    logger.info("HOST_DATA_FOLDER: %s", str(os.environ.get("HOST_DATA_FOLDER")))

    if is_docker:
        logger.info("Detected running inside Docker container.")
        DATA_FOLDER = str(os.environ.get("CONTAINER_DATA_FOLDER"))
    elif not is_docker:
        logger.info("Detected running on host machine.")
        DATA_FOLDER = str(os.environ.get("HOST_DATA_FOLDER"))

    if Path(DATA_FOLDER).exists():
        logger.info("DATA_FOLDER: %s", DATA_FOLDER)
    else:
        e = f"{Path(DATA_FOLDER)!s} not found or does not exist."
        logger.exception(NotADirectoryError(e))
        raise NotADirectoryError(e)

    return DATA_FOLDER
