# Instructions

## Python

First install `pyonb_docling`. From the top-level `pyonb` directory:

```shell
uv sync --extra docling
```

Then, to convert a PDF to markdown:

```python
import pyonb_docling

result = pyonb_docling.convert_pdf_to_markdown(
    file_path="path/to/data/input.pdf",
)
```

## Docker Compose

From the `pyonb/packages/ocr/docling` directory:

```shell
docker compose run docling data/input.pdf data/output.md
```

Note, you will need to set `DATA_FOLDER` in a `.env` file,
e.g: `DATA_FOLDER=path/to/data/input.pdf`
