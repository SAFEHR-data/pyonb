# Instructions

Before using the `kreuzberg` API for OCR, you will need to set the `KREUZBERG_API_PORT`
environment variable in the top-level `.env` file.

## Python

First install the `kreuzberg` API. From the top-level `pyonb` directory:

```shell
uv sync -extra kreuzberg
```

Then start the `kreuzberg` API:

```shell
python src/pyonb_kreuzberg/api.py
```

You can then use `curl` to send a PDF to the API:

```shell
curl -v -X POST http://127.0.0.1:8111/extract \
  -F "file_upload=@document.pdf" \
  -H "accept: application/json"
```

Note, this assumes you have set `KREUZBERG_API_PORT=8111`.

Currently, this returns the response from the
[`kreuzberg` API](https://kreuzberg.dev/user-guide/api-server/#extract-files)
directly, rather than the standard `pyonb` response.

## Docker Compose

You will need to define the `OCR_FORWARDING_API_PORT` in the `.env` file.

Then, spin up the `ocr-forwarding-api` and `kreuzberg` services:

```shell
docker-compose --profile kreuzberg up --build --detach
```

You can then use `curl` to send a PDF to the forwarding API:

```shell
curl -v -X POST http://127.0.0.1:8110/kreuzberg-ocr/inference_single \
  -F "file_upload=@document.pdf" \
  -H "accept: application/json"
```

Note, this assumes you have set `OCR_FORWARD_API_PORT` to `8110`.
