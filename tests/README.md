# Tests

## Test Directories

The `tests/` folder contains the following directories:

- `analysis/` - for testing the OCR evaluation metrics code
- `api/` - for testing API availability and OCR processing endpoints
- `data/single_synthetic_doc` - single synthetic PDF typically used in POST request to API endpoint
- `data/multiple_synthetic_docs` - synthetic documents for testing pyonb batch processing when pointed at a folder containing multiple documents
- `data/ocr_eval` - files for testing OCR evaluation metrics. The `.txt` file is a copy-pasted version of the file in `data/single_synthetic_doc` for use as a ground truth. The `.json` file is the output from Marker OCR.

## Automated Testing

pyonb uses GitHub Actions for automated testing. The [`tests.yaml` GitHub Action](../.github/workflows/tests.yml) spins up the OCR Forwarding API and a single OCR service (Marker) against which to run unit tests. Automated testing is not performed across all OCR tools to save GitHub minutes. For testing the other OCR tools, perform local testing.

## Local Execution

**Recommended:** run unit tests against specific OCR tool APIs. For example, if you raise the Marker and Docling OCR services, do not run the Paddle unit tests as they will fail.

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

4. Edit `.env` to set the `HOST_DATA_FOLDER` to point at your local `/tests/data/single_synthetic_doc` directory

5. Start the Docker services using your chosen OCR tools, e.g.:

```sh
docker compose --profile marker --profile docling up -d
```

6. Run tests using tox (inference may take ~minutes):

```sh
tox -e py312
```

To run unit tests individually, adapt the following to your chosen OCR tool:

```sh
tox -e py312 -- tests/api/test_routers.py::test_inference_single_file_upload_marker
```

## Troubleshooting

> The tests are failing!

- Have you copied `.env.tests` to root and renamed it `.env`?
- Have you set the environment variables in `.env`?

> I'm running the tests locally and they are failing!

- Have you exported the environment variables on your local machine?

> Some of the tests are passing, but some are failing!

- Have you run tests for OCR tools which you have not raised via `docker compose`?

> I am running an OCR inference test, but it is taking ages!

- Is your internet connection slow? Some of the OCR tools install Nvidia drivers which can take a while.

> The containers are building but one of the OCR tools is not working!

- Do you have appropriate user permissions on your machine? Some of the OCR tools download files (model weights etc.), which require internet access and local write permission.

> The containers are building but when I go to `http://localhost:PORT_XXXX` I don't see Swagger!

- Is something already running on `PORT_XXXX`?
- Have you tried changing the port in `.env` to something else?
