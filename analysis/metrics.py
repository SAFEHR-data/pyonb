"""OCR tool performance metrics."""

import Levenshtein


def cer(gt: str, pred: str) -> float:
    """
    Character Error Rate (CER): edit distance / length of ground truth.

    CER = 0 - Perfect character match
    CER = 1 - Completely different
    """
    if not gt:
        return float("inf") if pred else 0.0
    return round(Levenshtein.distance(gt, pred) / len(gt), 3)


def wer(gt: str, pred: str) -> float:
    """
    Word Error Rate (WER): edit distance over tokenized words.

    WER = 0 - Perfect word match
    WER = 1 - Completely different
    """
    gt_words = gt.split()
    pred_words = pred.split()
    return round(Levenshtein.distance(" ".join(gt_words), " ".join(pred_words)) / max(1, len(gt_words)), 3)


def emr(gt_list: list[str], pred_list: list[str]) -> float:
    """Exact Match Rate (EMR): % of predictions that match the ground truth exactly."""
    if len(gt_list) == len(pred_list):
        msg = "Mismatched list lengths."
        raise ValueError(msg)
    matches = sum(gt == pred for gt, pred in zip(gt_list, pred_list, strict=False))
    return matches / len(gt_list)


def ned(gt: str, pred: str) -> float:
    """
    Normalized Edit Distance: edit distance / max length.

    NED = 0 - Perfect match, strings identical
    NED = 1 - Maximum dissimilarity
    """
    max_len = max(len(gt), len(pred))
    if max_len == 0:
        return 0.0
    return round(Levenshtein.distance(gt, pred) / max_len, 3)
