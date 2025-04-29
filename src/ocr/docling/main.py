import os
import sys
from docling.document_converter import DocumentConverter


def convert_pdf_to_markdown(file_path):
    """
    Convert the PDF to Markdown using Docling.
    """
    try:
        print(f"CWD: {os.getcwd()}")
        print(f"LISTDIR: {os.listdir()}")

        converter = DocumentConverter()
        result = converter.convert(file_path)
        
        print(f"Docling output:")
        print(result.document.export_to_markdown())  # nb: markdown for terminal display

        return result.document.export_to_text()
    
    except Exception as e:
        print(f"Error processing PDF: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_pdf_path> <output_txt_path>")
        sys.exit(1)

    # TODO: more robust file pathing - Python and Docker
    input_pdf_path = sys.argv[1]
    output_txt_path = sys.argv[2]

    res = convert_pdf_to_markdown(
        file_path=input_pdf_path
        )

    try:
        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write(res)

        print(f"Text extracted to {output_txt_path}")
    
    except Exception as e:
        print(f"Error writing OCR output to textfile: {e}")
