## Instructions

### Python

NB: below MUST have absolute paths
```shell
cd pyonb/ocr/docling
python main.py ../tests/ms-note-one-page.pdf ../tests/output.txt
```

### Docker Compose

NB: Set DATA_FOLDER in .env, e.g: DATA_FOLDER=path/to/folder/containing/PDF
```shell
cd pyonb/ocr/docling
docker compose run docling data/ms-note-one-page.pdf data/output.txt
```

