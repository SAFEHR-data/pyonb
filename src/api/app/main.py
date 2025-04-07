from fastapi import FastAPI
from .routers import sparrow, marker

app = FastAPI()

app.include_router(sparrow.router)
app.include_router(marker.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
