import os
from kreuzberg._api.main import app
import uvicorn

KREUZBERG_API_PORT = os.getenv("KREUZBERG_API_PORT")

uvicorn.run(
    app,
    host="0.0.0.0",
    port=KREUZBERG_API_PORT,
    workers=4,
    reload=True,
    use_colors=True,
)

