"""Test OCR evaluation code."""

from ast import literal_eval
from pathlib import Path

from analysis.eval_ocr import evaluate_metrics, read_file


def test_read_file(ground_truth_txt_filepath: Path, marker_ocr_json_filepath: Path) -> None:
    """Test read_file."""
    gt_text = read_file(ground_truth_txt_filepath)
    ocr_json = read_file(marker_ocr_json_filepath)

    assert isinstance(gt_text, str)
    assert isinstance(ocr_json, dict)


def test_evaluate_metrics(ground_truth_txt_filepath: Path, marker_ocr_json_filepath: Path) -> None:
    """
    Test OCR evaluation metrics.

    - Character Error Rate
    - Word Error Rate
    - Exact Match Rate
    - Normalised Edit Distance

    Assumes:
    - ground_truth_txt_filepath = .txt loaded as str
    - marker_ocr_json_filepath = .txt loaded as str, or, .json subsequently converted to str
    """
    gt_file_output = str(read_file(ground_truth_txt_filepath))
    ocr_file_output = read_file(marker_ocr_json_filepath)

    if isinstance(ocr_file_output, str):
        results = evaluate_metrics(str(gt_file_output), str(ocr_file_output))
    elif isinstance(ocr_file_output, dict):
        ocr_text = literal_eval(ocr_file_output["ocr-result"])
        results = evaluate_metrics(str(gt_file_output), ocr_text)
    else:
        msg = "OCR file is not .txt or .json."
        raise TypeError(msg)

    assert results["cer"] > 0
    assert results["wer"] > 0
    assert results["ned"] > 0
