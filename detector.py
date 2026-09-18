"""
detector.py
-----------
Core logic for the Mutation Detector project:
  - sequence validation
  - alignment (via align.py)
  - position-by-position comparison
  - mutation classification (substitution, insertion, deletion)
"""

from dataclasses import dataclass
from align import align_sequences, GAP_CHAR

VALID_BASES = set("ATGC")


@dataclass
class Mutation:
    position: int          # 1-based position in the reference sequence
    reference_base: str
    sample_base: str
    mutation_type: str      # "Substitution", "Insertion", or "Deletion"


def read_fasta(path: str) -> str:
    """Reads a single-sequence FASTA file and returns the sequence as a string."""
    sequence_lines = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(">"):
                continue
            sequence_lines.append(line.upper())
    return "".join(sequence_lines)


def validate_sequence(sequence: str) -> bool:
    """Checks that a sequence contains only valid DNA bases (A, T, G, C)."""
    if not sequence:
        return False
    return set(sequence.upper()) <= VALID_BASES


def detect_mutations(reference: str, sample: str):
    """
    Aligns the reference and sample sequences, then walks the alignment
    position by position to classify each difference.

    Returns:
        mutations: list of Mutation objects
        aligned_reference: aligned reference string (with gaps)
        aligned_sample: aligned sample string (with gaps)
    """
    aligned_reference, aligned_sample = align_sequences(reference, sample)

    mutations = []
    ref_position = 0  # tracks position in the ORIGINAL (ungapped) reference

    for ref_char, sample_char in zip(aligned_reference, aligned_sample):
        if ref_char != GAP_CHAR:
            ref_position += 1  # only advance reference position on real ref bases

        if ref_char == sample_char:
            continue  # identical base, no mutation

        if ref_char == GAP_CHAR:
            # extra base in sample not present in reference -> insertion
            mutations.append(
                Mutation(
                    position=ref_position,
                    reference_base="-",
                    sample_base=sample_char,
                    mutation_type="Insertion",
                )
            )
        elif sample_char == GAP_CHAR:
            # base present in reference but missing in sample -> deletion
            mutations.append(
                Mutation(
                    position=ref_position,
                    reference_base=ref_char,
                    sample_base="-",
                    mutation_type="Deletion",
                )
            )
        else:
            # both positions have a base, but they differ -> substitution
            mutations.append(
                Mutation(
                    position=ref_position,
                    reference_base=ref_char,
                    sample_base=sample_char,
                    mutation_type="Substitution",
                )
            )

    return mutations, aligned_reference, aligned_sample
