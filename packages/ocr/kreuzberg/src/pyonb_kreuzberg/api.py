"""API for Kreuzberg OCR."""

import os

import uvicorn
from kreuzberg._api.main import app

KREUZBERG_API_PORT = os.getenv("KREUZBERG_API_PORT")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=KREUZBERG_API_PORT,
        workers=4,
        reload=True,
        use_colors=True,
    )
