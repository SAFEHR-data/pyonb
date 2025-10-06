"""OCR tool performance metrics."""

import Levenshtein


def cer(gt: str, pred: str) -> float:
    """
    Character Error Rate (CER): edit distance / length of ground truth.

    CER = 0 - Perfect character match
    CER > 0 - ratio of character edits needed; values > 1.0 indicate more edits than original characters
    """
    if not gt:
        return float("inf") if pred else 0.0
    return round(Levenshtein.distance(gt, pred) / len(gt), 3)


def wer(gt: str, pred: str) -> float:
    """
    Word Error Rate (WER): edit distance over tokenized words.

    WER = 0 - Perfect word match
    WER > 0 - ratio of word edits needed; values > 1.0 indicate more edits than original words'
    """
    gt_words = gt.split()
    pred_words = pred.split()

    # Initialise dynamic programming matrix for edit distance calculation
    dp = [[0] * (len(pred_words) + 1) for _ in range(len(gt_words) + 1)]

    for i in range(len(gt_words) + 1):
        dp[i][0] = i
    for j in range(len(pred_words) + 1):
        dp[0][j] = j

    for i in range(1, len(gt_words) + 1):
        for j in range(1, len(pred_words) + 1):
            cost = 0 if gt_words[i - 1] == pred_words[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # deletion
                dp[i][j - 1] + 1,  # insertion
                dp[i - 1][j - 1] + cost,  # substitution
            )

    return round(dp[len(gt_words)][len(pred_words)] / max(1, len(gt_words)), 3)


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
    NED = 1 - all characters changed to make strings identical
    """
    max_len = max(len(gt), len(pred))
    if max_len == 0:
        return 0.0
    return round(Levenshtein.distance(gt, pred) / max_len, 3)
