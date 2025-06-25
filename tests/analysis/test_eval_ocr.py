"""Test OCR evaluation code."""

from ast import literal_eval
from pathlib import Path

from analysis.eval_ocr import evaluate_metrics, read_file


def test_evaluate_metrics(ground_truth_txt_filepath: Path, marker_ocr_json_filepath: Path) -> None:
    """
    Test OCR evaluation metrics.

    - Character Error Rate
    - Word Error Rate
    - Exact Match Rate
    - Normalised Edit Distance
    """
    gt_text = read_file(ground_truth_txt_filepath)
    ocr_json = read_file(marker_ocr_json_filepath)
    ocr_text = literal_eval(ocr_json["ocr-result"])  # convert \\n to \n

    results = evaluate_metrics(gt_text, ocr_text)
    assert results["cer"] > 0
    assert results["wer"] > 0
    assert results["emr"] > 0
    assert results["ned"] > 0
