FROM python:3.12.10-slim-bookworm

WORKDIR /app
RUN chmod -R u+x /app

COPY app/api.py requirements.txt ./

RUN apt-get update \
    && apt-get install -y curl build-essential ffmpeg libsm6 libxext6 poppler-utils libpoppler-cpp-dev pkg-config

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install paddlepaddle==3.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/

RUN pip install torch==2.6.0+cpu torchvision==0.21.0+cpu torchaudio==2.6.0+cpu --index-url https://download.pytorch.org/whl/cpu

CMD ["python", "api.py"]
