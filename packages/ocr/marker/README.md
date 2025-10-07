# Instructions

## Python

First install `pyonb_marker`. From the top-level `pyonb` directory:

```shell
uv sync --extra marker
```

Then, to convert a PDF to markdown:

```python
import pyonb_marker

result = pyonb_maker.convert_pdf_to_markdown(
    filepath="path/to/data/input.pdf",
)
```

## Docker compose

From the `pyonb/packages/ocr/marker` directory:

```shell
docker compose run marker data/ms-note-one-page.pdf data/output.md
```

Note, you will need to set `DATA_FOLDER` in a `.env` file,
e.g.: `DATA_FOLDER=path/to/data/input.pdf`.
