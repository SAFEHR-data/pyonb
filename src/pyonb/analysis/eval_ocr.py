"""Script to run and evaluate OCR performance metrics."""

import argparse
import json
from ast import literal_eval
from pathlib import Path

from pyonb.analysis.metrics import cer, ned, wer


def read_file(file_path: Path) -> str | dict:
    """Read .txt or .json file."""
    with Path.open(file_path, "r") as f:
        file_type = file_path.suffix.lower()

        if file_type == ".json":
            output = json.load(f)
        elif file_type in (".txt", ".text"):
            output = f.read()
        else:
            e = f"Unsupported file type: {file_type}"
            raise ValueError(e)
        return output


def evaluate_metrics(gt_text: str, ocr_text: str) -> dict:
    """Run and evaluate OCR tool performance metrics."""
    cer_result = cer(gt_text, ocr_text)
    wer_result = wer(gt_text, ocr_text)
    ned_result = ned(gt_text, ocr_text)
    return {"cer": cer_result, "wer": wer_result, "ned": ned_result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run and evaluate OCR performance metrics.")
    parser.add_argument("-gt", "--ground_truth_file", type=str, required=True, help="[.txt] Path to ground truth file.")
    parser.add_argument("-ocr", "--ocr_file", type=str, required=True, help="[.json/.txt] Path to OCR processed file.")
    args = parser.parse_args()

    gt_file_output = read_file(Path(args.ground_truth_file))
    ocr_file_output = read_file(Path(args.ocr_file))

    if isinstance(ocr_file_output, str):
        result = evaluate_metrics(str(gt_file_output), str(ocr_file_output))
    elif isinstance(ocr_file_output, dict):
        ocr_text = literal_eval(ocr_file_output["ocr-result"])
        result = evaluate_metrics(str(gt_file_output), ocr_text)
    else:
        msg = "OCR file is not .txt or .json."
        raise TypeError(msg)

    print(f"OCR Evaluation results:\n{result}")  # noqa: T201
