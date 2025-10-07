# `pyonb` forwarding API

The forwarding API is used to send documents to an OCR service for processing. It provides a consistent
interface for using the various OCR tools supported by `pyonb`.

## Usage

You will need to define the `OCR_FORWARDING_API_PORT` in a `.env` file.

Then, spin up the `ocr-forwarding-api` servicer, along with the OCR service you wish to use.
For example, if you would like to use `kreuzberg`, run the following from the top-level `pyonb` directory:

```shell
docker-compose --profile kreuzberg up --build --detach
```

You can then use `curl` to send a PDF to the forwarding API:

```shell
curl -v -X POST http://127.0.0.1:8110/kreuzberg-ocr/inference_single \
  -F "file_upload=@document.pdf" \
  -H "accept: application/json"
```

Note, this assumes you have set `OCR_FORWARDING_API_PORT` to `8110`.
