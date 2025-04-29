import sys
from marker.config.parser import ConfigParser
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered


# Initialize PDF converter object
def setup_converter(config, config_parser):
    artifact_dict = create_model_dict()
    converter = PdfConverter(artifact_dict=artifact_dict, config=config, llm_service=config_parser.get_llm_service())
    return converter


def convert_pdf_to_markdown(file_path, output_format="markdown", use_llm=True):
    """
    Convert the PDF to markdown using Marker and optionally use LLM for improved accuracy.
    """
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
        rendered = converter(file_path)
        
        # Extract the text (Markdown, JSON, or HTML) from the rendered object
        text, _, images = text_from_rendered(rendered)

        return text, images
    
    except Exception as e:
        print(f"Error processing PDF: {e}")

def run_marker(input_pdf_path):
    """
    Execute marker.
    """
    res, images = convert_pdf_to_markdown(
        file_path=input_pdf_path,
        use_llm=True,
        output_format="json"
        )
    
    return res, images

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_pdf_path> <output_txt_path>")
        sys.exit(1)

    # TODO: more robust file pathing - Python and Docker
    input_pdf_path = sys.argv[1]
    output_txt_path = sys.argv[2]

    res, images = run_marker(input_pdf_path)

    try:
        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write(res)

        print(f"Text extracted to {output_txt_path}")
    
    except Exception as e:
        print(f"Error writing OCR output to textfile: {e}")
