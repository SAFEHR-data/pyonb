FROM paddlepaddle/paddle:3.0.0

WORKDIR /app
RUN chmod -R u+x /app

COPY app/api.py requirements.txt ./

RUN apt-get update \
    && apt-get install -y curl build-essential ffmpeg libsm6 libxext6 poppler-utils libpoppler-cpp-dev pkg-config

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "api.py"]
