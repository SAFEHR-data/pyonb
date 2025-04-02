from fastapi import FastAPI
from .routers import sparrow

app = FastAPI()

app.include_router(sparrow.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
