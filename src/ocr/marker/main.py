"""Marker OCR runner."""

import logging
import sys
from pathlib import Path

from marker.config.parser import ConfigParser
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

logger = logging.getLogger()


def setup_converter(config, config_parser) -> PdfConverter:  # noqa: ANN001
    """Initialize PDF converter object."""
    artifact_dict = create_model_dict()
    return PdfConverter(
        artifact_dict=artifact_dict,
        config=config,
        llm_service=config_parser.get_llm_service(),
    )


def convert_pdf_to_markdown(file_path: str | Path, output_format: str | Path = "markdown", use_llm: bool = True):  # noqa: ANN201
    """Convert the PDF to markdown using Marker and optionally use LLM for improved accuracy."""
    try:
        # Optionally enable LLM for improved accuracy
        config = {
            "output_format": output_format,
            "use_llm": use_llm,
            "llm_service": "marker.services.ollama.OllamaService",
            "ollama_model": "llama3.2",
            "ollama_base_url": "http://localhost:11434",
        }
        config_parser = ConfigParser(config)
        # Create the converter with the necessary settings
        converter = setup_converter(config_parser.generate_config_dict(), config_parser)

        # Process the PDF file and convert to the specified output format
        rendered = converter(str(file_path))

        # Extract the text (Markdown, JSON, or HTML) from the rendered object
        text, _, images = text_from_rendered(rendered)
    except Exception:
        logger.exception("Error processing PDF.")
    else:
        return text, images


def run_marker(input_pdf_path: str | Path):  # noqa: ANN201
    """Execute marker."""
    res, images = convert_pdf_to_markdown(file_path=input_pdf_path, use_llm=True, output_format="json")

    return res, images


if __name__ == "__main__":
    if len(sys.argv) != 3:  # noqa: PLR2004
        logger.exception("Usage: python main.py <input_pdf_path> <output_txt_path>")
        sys.exit(1)

    # TODO(tom): more robust file pathing - Python and Docker
    input_pdf_path = Path(sys.argv[1])
    output_txt_path = Path(sys.argv[2])

    res, images = run_marker(input_pdf_path)

    try:
        with output_txt_path.open("w", encoding="utf-8") as f:
            f.write(res)

        logger.info("Text extracted to %s", output_txt_path)

    except Exception:
        logger.exception("Error writing OCR output to textfile.")
