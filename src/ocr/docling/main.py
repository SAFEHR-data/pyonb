"""Docling OCR runner."""

import logging
import sys
from pathlib import Path

from docling.document_converter import DocumentConverter

logger = logging.getLogger()


def convert_pdf_to_markdown(file_path: str | Path):  # noqa: ANN201
    """Convert the PDF to Markdown using Docling."""
    try:
        logger.info("CWD: %s", Path.cwd())
        logger.info("LISTDIR: %s", list(Path("some_directory").iterdir()))

        converter = DocumentConverter()
        result = converter.convert(file_path)

        logger.info("Docling output:")
        logger.info(result.document.export_to_markdown())  # nb: markdown for terminal display

        return result.document.export_to_text()

    except Exception:
        logger.exception("Error processing PDF.")


if __name__ == "__main__":
    if len(sys.argv) != 3:  # noqa: PLR2004
        logger.info("Usage: python main.py <input_pdf_path> <output_txt_path>")
        sys.exit(1)

    # TODO(tom): more robust file pathing - Python and Docker
    input_pdf_path = Path(sys.argv[1])
    output_txt_path = Path(sys.argv[2])

    res = convert_pdf_to_markdown(file_path=input_pdf_path)

    try:
        with output_txt_path.open("w", encoding="utf-8") as f:
            f.write(res)

        logger.exception("Text extracted to %s", output_txt_path)

    except Exception:
        logger.exception("Error writing OCR output to textfile.")
