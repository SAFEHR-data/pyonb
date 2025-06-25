"""OCR tool performance metrics."""

import Levenshtein


def cer(gt: str, pred: str) -> float:
    """Character Error Rate (CER): edit distance / length of ground truth."""
    if not gt:
        return float("inf") if pred else 0.0
    return Levenshtein.distance(gt, pred) / len(gt)


def wer(gt: str, pred: str) -> float:
    """Word Error Rate (WER): edit distance over tokenized words."""
    gt_words = gt.split()
    pred_words = pred.split()
    return Levenshtein.distance(" ".join(gt_words), " ".join(pred_words)) / max(1, len(gt_words))


def emr(gt_list: list[str], pred_list: list[str]) -> float:
    """Exact Match Rate (EMR): % of predictions that match the ground truth exactly."""
    if len(gt_list) == len(pred_list):
        msg = "Mismatched list lengths."
        raise ValueError(msg)
    matches = sum(gt == pred for gt, pred in zip(gt_list, pred_list, strict=False))
    return matches / len(gt_list)


def ned(gt: str, pred: str) -> float:
    """Normalized Edit Distance: edit distance / max length."""
    max_len = max(len(gt), len(pred))
    if max_len == 0:
        return 0.0
    return Levenshtein.distance(gt, pred) / max_len
