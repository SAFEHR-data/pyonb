## Tests

### Test Directories

The `tests/` folder contains the following directories:
- `analysis/` - for testing the OCR evaluation metrics code
- `api/` - for testing API availability and OCR processing endpoints
- `data/single_synthetic_doc` - single synthetic PDF typically used in POST request to API endpoint
- `data/multiple_synthetic_docs` - synthetic documents for testing pyonb batch processing when pointed at a folder containing multiple documents
- `data/ocr_eval` - files for testing OCR evaluation metrics. The `.txt` file is a copy-pasted version of the file in `data/single_synthetic_doc` for use as a ground truth. The `.json` file is the output from Marker OCR.

### Automated Testing

pyonb uses GitHub Actions for automated testing. The [`tests.yaml` GitHub Action](../.github/workflows/tests.yml) spins up the OCR Forwarding API and a single OCR service (Marker) against which to run unit tests. Automated testing is not performed across all OCR tools to save GitHub minutes. For testing the other OCR tools, perform local testing.

### Local Execution

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