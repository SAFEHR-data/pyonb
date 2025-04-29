> [!WARNING]  
> This repo is under construction.

# pyonb

<!--COMMENT OUT

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Tests status][tests-badge]][tests-link]
[![Linting status][linting-badge]][linting-link]
[![Documentation status][documentation-badge]][documentation-link]
[![License][license-badge]](./LICENSE.md)

END COMMENT OUT-->

<!-- prettier-ignore-start -->
[tests-badge]:              https://github.com/SAFEHR-data/pyonb/actions/workflows/tests.yml/badge.svg
[tests-link]:               https://github.com/SAFEHR-data/pyonb/actions/workflows/tests.yml
[linting-badge]:            https://github.com/SAFEHR-data/pyonb/actions/workflows/linting.yml/badge.svg
[linting-link]:             https://github.com/SAFEHR-data/pyonb/actions/workflows/linting.yml
[documentation-badge]:      https://github.com/SAFEHR-data/pyonb/actions/workflows/docs.yml/badge.svg
[documentation-link]:       https://github.com/SAFEHR-data/pyonb/actions/workflows/docs.yml
[license-badge]:            https://img.shields.io/badge/License-MIT-yellow.svg
<!-- prettier-ignore-end -->

- Python SDK for OnBase REST API (eventually)
- Optical Character Recognition (OCR) API for converting PDFs to structured text
- Planned OCR tool compatibility:
   - marker
   - docling
   - sparrow

## Getting Started

### Prerequisites

`pyonb` requires Docker and Docker Compose.

### Installation & Usage

1. Rename `.env.sample` to `.env`.

2. Edit `.env` with the correct `HOST_DATA_FOLDER` location, e.g.:

```sh
HOST_DATA_FOLDER="/absolute/path/to/pyonb/src/ocr/tests/synthetic_docs"
```

4. Set OCR service ports, e.g.:

```sh
OCR_FORWARDING_API_PORT=8080
SPARROW_API_PORT=8001
MARKER_API_PORT=8002
```

> [!IMPORTANT] 
> For GAE usage, set OCR service ports and UCLH proxy details:
> ```sh
> http_proxy=
> https_proxy=
> HTTPS_PROXY=
> HTTP_PROXY=
> ```

5. Start the OCR API Server (e.g. using Sparrow and marker):

```sh
docker compose --profile sparrow --profile marker up -d
```

6. Open FastAPI Swagger at http://127.0.0.1:8080/docs to view and execute endpoints.

The following POST endpoints will execute the OCR tool on all PDFs in the `HOST_DATA_FOLDER`:
- **sparrow** - POST `sparrow-ocr/inference`
- **marker** - POST `marker/inference`

7. View the JSON response:

<center><img src="docs/ocr-json-response-example.png" alt="OCR Server JSON response" width="75%"/></center>

### Developer Tips:
- Alternatively to Swagger, use [Postman](https://www.postman.com/) to construct, save and make your API requests.



<!--COMMENT OUT 
We recommend installing in a project specific virtual environment created using
a environment management tool such as
[Conda](https://docs.conda.io/projects/conda/en/stable/). To install the latest
development version of `pyonb` using `pip` in the currently active
environment run

```sh
pip install git+https://github.com/SAFEHR-data/pyonb.git
```

Alternatively create a local clone of the repository with

```sh
git clone https://github.com/SAFEHR-data/pyonb.git
```

and then install in editable mode by running

```sh
pip install -e .
```

### Running Locally

How to run the application on your local system.

### Running Tests

END COMMENT OUT-->

<!-- How to run tests on your local system. -->

<!--COMMENT OUT 

Tests can be run across all compatible Python versions in isolated environments
using [`tox`](https://tox.wiki/en/latest/) by running

```sh
tox
```

To run tests manually in a Python environment with `pytest` installed run

```sh
pytest tests
```

again from the root of the repository.

### Building Documentation

The MkDocs HTML documentation can be built locally by running

```sh
tox -e docs
```

from the root of the repository. The built documentation will be written to
`site`.

Alternatively to build and preview the documentation locally, in a Python
environment with the optional `docs` dependencies installed, run

```sh
mkdocs serve
```

END COMMENT OUT-->

## About

### Project Team

- Arman Eshaghi
- Tom Roberts ([tom.roberts@ucl.ac.uk](mailto:tom.roberts@ucl.ac.uk))
- Kawsar Noor
- Lawrence Lai

## Acknowledgements

This work was funded by the National Institute for Health and Care Research (NIHR, award code NIHR302495).

This project is developed in collaboration with the
[Centre for Advanced Research Computing](https://ucl.ac.uk/arc), University
College London.
