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


def convert_pdf_to_markdown(  # noqa: ANN201
    file_path: str | Path,
    output_format: str | Path = "markdown",
    use_llm: bool = True,
):
    """Convert the PDF to markdown using Marker and optionally use LLM for improved accuracy."""
    config = {
        "output_format": output_format,
        "use_llm": use_llm,
        "llm_service": "marker.services.ollama.OllamaService",
        "ollama_model": "llama3.2",
        "ollama_base_url": "http://localhost:11434",
        "disable_images": True,
    }
    config_parser = ConfigParser(config)
    converter = setup_converter(config_parser.generate_config_dict(), config_parser)
    try:
        rendered = converter(str(file_path))
        text, _, _ = text_from_rendered(rendered)
    except Exception:
        logger.exception("Error processing PDF.")

    return text


if __name__ == "__main__":
    if len(sys.argv) != 3:  # noqa: PLR2004
        logger.exception("Usage: python main.py <input_pdf_path> <output_txt_path>")
        sys.exit(1)

    # TODO(tom): more robust file pathing - Python and Docker
    input_pdf_path = Path(sys.argv[1])
    output_txt_path = Path(sys.argv[2])

    text = convert_pdf_to_markdown(input_pdf_path)

    try:
        with output_txt_path.open("w", encoding="utf-8") as f:
            f.write(text)

        logger.info("Text extracted to %s", output_txt_path)

    except Exception:
        logger.exception("Error writing OCR output to textfile.")
