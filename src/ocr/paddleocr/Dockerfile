FROM paddlepaddle/paddle:3.0.0

COPY . /
COPY requirements.txt /app

RUN apt-get update \
    && apt-get install -y curl build-essential ffmpeg libsm6 libxext6 poppler-utils libpoppler-cpp-dev pkg-config

RUN pip install -U pip
RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ["python", "api.py"]
