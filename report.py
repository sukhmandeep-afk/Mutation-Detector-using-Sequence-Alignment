"""
report.py
---------
Turns a list of detected Mutation objects into a results table (Pandas),
a summary of counts, a CSV file, and a bar chart (Matplotlib).
"""

import pandas as pd
import matplotlib.pyplot as plt


def mutations_to_dataframe(mutations) -> pd.DataFrame:
    """Converts a list of Mutation objects into a Pandas DataFrame."""
    rows = [
        {
            "Position": m.position,
            "Reference Base": m.reference_base,
            "Sample Base": m.sample_base,
            "Mutation Type": m.mutation_type,
        }
        for m in mutations
    ]
    columns = ["Position", "Reference Base", "Sample Base", "Mutation Type"]
    return pd.DataFrame(rows, columns=columns)


def summarize_mutations(mutations) -> dict:
    """Returns counts of total mutations and each mutation type."""
    summary = {
        "Total Mutations": len(mutations),
        "Substitutions": sum(1 for m in mutations if m.mutation_type == "Substitution"),
        "Insertions": sum(1 for m in mutations if m.mutation_type == "Insertion"),
        "Deletions": sum(1 for m in mutations if m.mutation_type == "Deletion"),
    }
    return summary


def save_report_csv(df: pd.DataFrame, path: str):
    """Saves the mutation results table as a CSV file."""
    df.to_csv(path, index=False)


def save_summary_chart(summary: dict, path: str):
    """Creates and saves a simple bar chart of mutation type counts."""
    labels = ["Substitutions", "Insertions", "Deletions"]
    values = [summary["Substitutions"], summary["Insertions"], summary["Deletions"]]
    colors = ["#4C72B0", "#DD8452", "#55A868"]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels, values, color=colors)
    ax.set_title("Mutation Types Detected")
    ax.set_ylabel("Count")
    ax.bar_label(bars, padding=3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def print_console_report(summary: dict, df: pd.DataFrame):
    """Prints a readable report to the console."""
    print("\n" + "=" * 50)
    print("MUTATION DETECTION REPORT")
    print("=" * 50)
    print(f"Total Mutations Found : {summary['Total Mutations']}")
    print(f"  Substitutions       : {summary['Substitutions']}")
    print(f"  Insertions          : {summary['Insertions']}")
    print(f"  Deletions           : {summary['Deletions']}")
    print("-" * 50)
    if df.empty:
        print("No mutations detected. Sequences are identical.")
    else:
        print(df.to_string(index=False))
    print("=" * 50 + "\n")
