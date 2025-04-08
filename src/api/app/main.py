import logging
import datetime
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from .routers import sparrow, marker


logging.basicConfig(filename="pyonb-" + datetime.datetime.now().strftime("%Y_%m_%d") + ".log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = FastAPI()

app.include_router(sparrow.router)
app.include_router(marker.router)

@app.get("/")
async def health_check():
    """
    Health check endpoint to verify API is accessible.
    Returns 200 OK status if API is running properly.
    """
    return JSONResponse(status_code=status.HTTP_200_OK, content={"service": "pyonb-ocr-api", "status": "healthy"})
