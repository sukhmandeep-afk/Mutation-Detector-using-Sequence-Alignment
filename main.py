"""
main.py
-------
Command-line entry point for the Mutation Detector Using Sequencing Alignment.

Usage:
    python main.py --reference sample_data/reference.fasta --sample sample_data/sample.fasta
    python main.py --reference ATGCTACCGT --sample ATGCTACAGT   (raw sequences also work)

Output:
    - Console report
    - output/mutation_report.csv
    - output/mutation_chart.png
"""

import argparse
import os
import sys

from detector import read_fasta, validate_sequence, detect_mutations
from report import (
    mutations_to_dataframe,
    summarize_mutations,
    save_report_csv,
    save_summary_chart,
    print_console_report,
)


def load_sequence(value: str) -> str:
    """Loads a sequence either from a FASTA file path or a raw string."""
    if os.path.isfile(value):
        return read_fasta(value)
    return value.strip().upper()


def main():
    parser = argparse.ArgumentParser(
        description="Detect substitution, insertion, and deletion mutations "
        "between a reference and a sample DNA sequence."
    )
    parser.add_argument(
        "--reference", required=True, help="Reference sequence (FASTA file path or raw sequence string)"
    )
    parser.add_argument(
        "--sample", required=True, help="Sample sequence (FASTA file path or raw sequence string)"
    )
    parser.add_argument(
        "--outdir", default="output", help="Directory to save the CSV report and chart (default: output/)"
    )
    args = parser.parse_args()

    reference = load_sequence(args.reference)
    sample = load_sequence(args.sample)

    # --- Step 1: Validation ---
    if not validate_sequence(reference):
        print("ERROR: Reference sequence contains invalid characters. Only A, T, G, C are allowed.")
        sys.exit(1)
    if not validate_sequence(sample):
        print("ERROR: Sample sequence contains invalid characters. Only A, T, G, C are allowed.")
        sys.exit(1)

    # --- Step 2-5: Align, compare, classify ---
    mutations, aligned_ref, aligned_sample = detect_mutations(reference, sample)

    print("\nAligned Reference : " + aligned_ref)
    print("Aligned Sample    : " + aligned_sample)

    # --- Step 6: Build results table + summary ---
    df = mutations_to_dataframe(mutations)
    summary = summarize_mutations(mutations)
    print_console_report(summary, df)

    # --- Step 7: Save outputs ---
    os.makedirs(args.outdir, exist_ok=True)
    csv_path = os.path.join(args.outdir, "mutation_report.csv")
    chart_path = os.path.join(args.outdir, "mutation_chart.png")

    save_report_csv(df, csv_path)
    save_summary_chart(summary, chart_path)

    print(f"Report saved to : {csv_path}")
    print(f"Chart saved to  : {chart_path}")


if __name__ == "__main__":
    main()
