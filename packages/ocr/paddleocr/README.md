# Instructions

Before using the `paddleocr` API for OCR, you will need to set the `PADDLEOCR_API_PORT`
environment variable in the top-level `.env` file.

## Docker Compose

You will need to define the `OCR_FORWARDING_API_PORT` in the `.env` file.

Then, spin up the `ocr-forwarding-api` and `kreuzberg` services:

```shell
docker-compose --profile paddleocr up --build --detach
```

You can then use `curl` to send a PDF to the forwarding API:

```shell
curl -v -X POST http://127.0.0.1:8110/paddleocr/inference_single \
  -F "file_upload=@document.pdf" \
  -H "accept: application/json"
```

Note, this assumes you have set `OCR_FORWARDING_API_PORT` to `8110`.
