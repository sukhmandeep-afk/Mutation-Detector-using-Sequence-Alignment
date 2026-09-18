"""
align.py
--------
Handles pairwise global alignment of two DNA sequences.

Uses Biopython's Align.PairwiseAligner if biopython is installed
(recommended - run: pip install biopython).
Falls back to a built-in Needleman-Wunsch implementation if
biopython is not available, so the project still runs out of the box.
"""

try:
    from Bio import Align
    BIOPYTHON_AVAILABLE = True
except ImportError:
    BIOPYTHON_AVAILABLE = False


GAP_CHAR = "-"


def _align_with_biopython(reference: str, sample: str):
    aligner = Align.PairwiseAligner()
    aligner.mode = "global"
    aligner.match_score = 2
    aligner.mismatch_score = -1
    aligner.open_gap_score = -2
    aligner.extend_gap_score = -0.5

    alignment = aligner.align(reference, sample)[0]
    aligned_ref, aligned_sample = alignment[0], alignment[1]
    return str(aligned_ref), str(aligned_sample)


def _align_with_fallback(reference: str, sample: str):
    """
    Simple Needleman-Wunsch global alignment implementation.
    Used only if Biopython isn't installed.
    """
    match_score = 2
    mismatch_score = -1
    gap_score = -2

    n, m = len(reference), len(sample)
    score = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        score[i][0] = i * gap_score
    for j in range(m + 1):
        score[0][j] = j * gap_score

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = score[i - 1][j - 1] + (
                match_score if reference[i - 1] == sample[j - 1] else mismatch_score
            )
            delete = score[i - 1][j] + gap_score
            insert = score[i][j - 1] + gap_score
            score[i][j] = max(match, delete, insert)

    aligned_ref, aligned_sample = [], []
    i, j = n, m
    while i > 0 and j > 0:
        current = score[i][j]
        diag = score[i - 1][j - 1]
        up = score[i - 1][j]
        left = score[i][j - 1]

        if current == diag + (
            match_score if reference[i - 1] == sample[j - 1] else mismatch_score
        ):
            aligned_ref.append(reference[i - 1])
            aligned_sample.append(sample[j - 1])
            i -= 1
            j -= 1
        elif current == up + gap_score:
            aligned_ref.append(reference[i - 1])
            aligned_sample.append(GAP_CHAR)
            i -= 1
        else:
            aligned_ref.append(GAP_CHAR)
            aligned_sample.append(sample[j - 1])
            j -= 1

    while i > 0:
        aligned_ref.append(reference[i - 1])
        aligned_sample.append(GAP_CHAR)
        i -= 1
    while j > 0:
        aligned_ref.append(GAP_CHAR)
        aligned_sample.append(sample[j - 1])
        j -= 1

    aligned_ref.reverse()
    aligned_sample.reverse()
    return "".join(aligned_ref), "".join(aligned_sample)


def align_sequences(reference: str, sample: str):
    """
    Returns (aligned_reference, aligned_sample) as equal-length strings,
    using '-' to represent gaps (insertions/deletions).
    """
    if BIOPYTHON_AVAILABLE:
        return _align_with_biopython(reference, sample)
    return _align_with_fallback(reference, sample)
