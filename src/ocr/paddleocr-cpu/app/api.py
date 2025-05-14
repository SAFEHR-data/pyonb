import datetime
import logging

import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from routers import paddleocr

logging.basicConfig(filename=datetime.datetime.now().strftime("%Y%m%d") + ".log",
                    format='%(asctime)s %(message)s',
                    filemode='a',
                    level=logging.DEBUG,
                    force=True)

# Creating an object
logger = logging.getLogger()


app = FastAPI()
app.include_router(paddleocr.router)

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint to verify API is accessible.
    Returns 200 OK status if API is running properly.
    """
    logger.info("[GET] /health")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"service": "paddleocr-cpu", "status": "healthy"})


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)