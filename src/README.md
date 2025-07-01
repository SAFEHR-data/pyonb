# src

This README explains the motivation for the design of the code in `src/` and describes some of the pertinent files.

pyonb is a set of APIs which was originally designed to sit within a document processing workflow between Hyland OnBase and [CogStack](https://github.com/cogstack). pyonb is used to perform OCR on documents fetched from OnBase (or any document store). The pyonb JSON response is passed to an outbound destination, such as a database.

pyonb incoporates a Forwarding API which passes the documents onto one of the included OCR tool APIs. This was created to have a single destination for inbound files and make it easy to pass files to different OCR tools. pyonb was also designed to make it easy to add in a new OCR tool.

## Docker Compose

The [`docker-compose.yaml`](../docker-compose.yml) in the root of the repository builds and connects all of the APIs the `src/` folder.

The APIs can be raised and used individually, without Docker Compose if you prefer, however you may encounter quirks and bugs as pyonb has been primarily designed as a suite of container services.

## src Directories

The `src/` folder contains the following directories:

- `api/` - Forwarding API and routers code associated with the OCR tools
   - `Dockerfile` - Builds the Forwarding API container
   - `app/main.py` - Forwarding API code entrypoint
   - `routers/**.py` - Forwarding API endpoints which connect to specified OCR tool endpoints
- `ocr/` - APIs and wrapper code for performing OCR processing
   - `docling/marker/etc.` - one directory per OCR tool
      - `Dockerfile` - Builds the OCR tool as a container service
      - `api.py` - Endpoints for the OCR tool
      - `main.py` - OCR tool execution code
   - *Note: Paddle uses a slightly different folder structure and Sparrow uses the folder structure of the host repo.*
- `pyonb/` - automated versioning code
