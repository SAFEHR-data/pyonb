from fastapi import FastAPI, status

app = FastAPI()

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """
    Health check endpoint to verify the API is accessible.
    Returns a 200 OK status if the API is running properly.
    """
    return {
        "status": "healthy",
        "service": "marker"
    }