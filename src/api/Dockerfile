FROM python:3.11.9-slim-bookworm

ADD . .

RUN apt-get update \
 && apt-get install -y vim curl

RUN pip install -U pip
RUN pip install -r requirements.txt

WORKDIR /app

CMD ["fastapi", "run", "main.py", "--port", "8080"]