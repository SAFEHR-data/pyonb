# pyonb

> [!WARNING]
> This repo is under construction.

<!--COMMENT OUT

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Tests status][tests-badge]][tests-link]
[![Linting status][linting-badge]][linting-link]
[![Documentation status][documentation-badge]][documentation-link]
[![License][license-badge]](./LICENSE.md)

END COMMENT OUT-->

**pyonb** is two things:

- a Python SDK for document extraction via the Hyland OnBase REST API (_work in progress_)
- a suite of APIs wrapped around open-source Optical Character Recognition (OCR) tools, designed for local deployment, for converting PDFs to structured text including:
  - [Marker](https://github.com/VikParuchuri/marker)
  - [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
  - [Docling](https://github.com/docling-project/docling)
  - [Kreuzberg](https://github.com/Goldziher/kreuzberg)

## Getting Started

### Prerequisites

`pyonb` requires Docker and Docker Compose.

### Installation & Usage

1. Rename `.env.sample` to `.env`.

2. Edit `.env` with the correct `HOST_DATA_FOLDER` location, e.g.:

```sh
HOST_DATA_FOLDER="/absolute/path/to/documents/folder"

# e.g. for unit tests on GAE:
# HOST_DATA_FOLDER="/gae/pyonb/tests/data/single_synthetic_doc"
```

4. Set OCR service ports, e.g.:

```sh
OCR_FORWARDING_API_PORT=8110
MARKER_API_PORT=8112
PADDLEOCR_API_PORT=8114
DOCLING_API_PORT=8115
```

> [!IMPORTANT]
> For GAE usage, set OCR service ports and UCLH proxy details:
>
> ```sh
> http_proxy=
> https_proxy=
> HTTPS_PROXY=
> HTTP_PROXY=
> ```

5. Start the OCR API Server (e.g. using marker and docling):

```sh
docker compose --profile marker --profile docling up -d
```

6. Open FastAPI Swagger at <http://127.0.0.1:8110/docs> to view and execute endpoints.

Use the following POST endpoints to execute the chosen OCR tool on a PDFs:

- **marker** - POST `/marker/inference_single`
- **docling** - POST `/docling/inference_single`

7. View the JSON response:

|                                                                 |
| :-------------------------------------------------------------: |
| ![OCR Server JSON response](docs/ocr-json-response-example.png) |

<!-- <div style="text-align:center;"></center> -->

### Developer Tips

- Alternatively to Swagger, use [Postman](https://www.postman.com/) to construct, save and make your API requests.

## Tests

1. Clone the repo:

```sh
git clone https://github.com/SAFEHR-data/pyonb.git
```

2. Create a virtual environment ([we suggest using uv](https://docs.astral.sh/uv/pip/environments/)) and install dependencies:

```sh
uv venv --python3.12
source .venv/bin/activate
uv sync
```

3. Copy the `tests/` .env file to root directory to use with tox:

```sh
cp /tests/.env.tests .env
```

4. Start the Docker services:

```sh
docker compose --profile marker --profile docling up -d
```

5. Run tests using tox:

```sh
tox -e py312
```

NB: this may take a few minutes to perform the inference tests. Some may fail depending on which OCR tools you choose to raise.
For example, with `--profile marker --profile docling` the Paddle and Kreuzberg APIs will not be raised,
so the associated tests will fail.

To run unit tests individually, adapt the following:

```sh
tox -e py312 -- tests/api/test_routers.py::test_inference_single_file_upload_marker
```

## About

### Project Team

- Arman Eshaghi
- Tom Roberts ([tom.roberts@ucl.ac.uk](mailto:tom.roberts@ucl.ac.uk))
- Kawsar Noor
- Lawrence Lai
- Stefan Piatek
- Richard Dobson
- Steve Harris
- Sarah Keating

## Acknowledgements

This work was funded by the National Institute for Health and Care Research (NIHR, award code NIHR302495).

This project is developed in collaboration with the
[Centre for Advanced Research Computing](https://ucl.ac.uk/arc), University
College London.
