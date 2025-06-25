"""Script to run and evaluate OCR performance metrics."""
import argparse
import json
from pathlib import Path

from analysis.metrics import cer, emr, ned, wer


def read_file(file_path: str | Path) -> str | dict:
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

def evaluate_metrics(gt_text: str, ocr_text: str) -> None:
    """Run and evaluate OCR tool performance metrics."""
    cer_result = cer(gt_text, ocr_text)
    wer_result = wer(gt_text, ocr_text)
    emr_result = emr(gt_text, ocr_text)
    ned_result = ned(gt_text, ocr_text)
    return {
        "cer": cer_result,
        "wer": wer_result,
        "emr": emr_result,
        "ned": ned_result
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run and evaluate OCR performance metrics."
    )
    parser.add_argument("-gt", "--ground_truth_file", type=str, required=True, help="Path to ground truth file.")
    parser.add_argument("-ocr", "--ocr_file", type=str, required=True, help="Path to OCR processed file.")
    args = parser.parse_args()

    gt_text = read_file(Path(args.ground_truth_file))
    ocr_text = read_file(Path(args.ocr_file))

    evaluate_metrics(gt_text, ocr_text)
