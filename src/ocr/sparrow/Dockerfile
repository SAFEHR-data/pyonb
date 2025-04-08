FROM python:3.10.4

RUN apt-get update \
    && apt-get install -y curl git ffmpeg libsm6 libxext6 poppler-utils libpoppler-cpp-dev

# Clone Sparrow repo
RUN git clone https://github.com/katanaml/sparrow.git /app

WORKDIR /app

RUN chmod -R u+x /app

# Install Sparrow packages
RUN pip install --upgrade pip
RUN pip install -r /app/sparrow-data/ocr/requirements.txt
RUN pip install -U python-poppler

CMD ["python", "/app/sparrow-data/ocr/api.py"]