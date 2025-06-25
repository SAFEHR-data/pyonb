# Use an official Python image
FROM python:3.11-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /app

# Copy app files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask flask-cors

# Ensure data folder exists
RUN mkdir -p /app/data

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
