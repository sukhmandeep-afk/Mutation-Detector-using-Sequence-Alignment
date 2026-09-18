# Mutation Detector Using Sequencing Alignment

A simple bioinformatics tool that compares a **reference** DNA sequence to a
**sample** DNA sequence and automatically detects **substitutions**,
**insertions**, and **deletions**.

This implements the full workflow from the project proposal:
`Input → Validation → Alignment → Comparison → Mutation Detection →
Classification → Result Table → Visualization → Report`

## Project Structure

```
mutation_detector/
├── align.py          # Sequence alignment (Biopython, with a built-in fallback)
├── detector.py        # Validation + mutation detection/classification logic
├── report.py           # Results table, summary, CSV export, chart
├── main.py               # Command-line entry point
├── app.py                    # Optional Streamlit web interface
├── sample_data/
│   ├── reference.fasta
│   └── sample.fasta
└── README.md
```

## Setup

```bash
pip install biopython pandas matplotlib streamlit
```

> Note: `biopython` and `streamlit` are optional. If they aren't installed,
> `main.py` still works — it automatically falls back to a built-in
> aligner. `streamlit` is only needed if you want the web UI (`app.py`).

## Usage

### Command line

Using raw sequences directly:
```bash
python main.py --reference ATGCTACCGT --sample ATGCTACAGT
```

Using FASTA files:
```bash
python main.py --reference sample_data/reference.fasta --sample sample_data/sample.fasta
```

This prints a report to the console and saves:
- `output/mutation_report.csv` — the mutation results table
- `output/mutation_chart.png` — a bar chart of mutation type counts

### Web interface (optional)

```bash
streamlit run app.py
```

Opens a browser page where you can paste sequences or upload FASTA files,
see the alignment, mutation table, chart, and download the CSV report.

## How It Works

1. **Validation** – checks that both sequences only contain A, T, G, C.
2. **Alignment** – aligns the reference and sample using a global alignment
   algorithm (Biopython's pairwise aligner, or a built-in Needleman-Wunsch
   implementation if Biopython isn't installed).
3. **Comparison** – walks through the alignment position by position.
4. **Classification**:
   - Same base in both → no mutation
   - Different base in both → **Substitution**
   - Gap in reference, base in sample → **Insertion**
   - Base in reference, gap in sample → **Deletion**
5. **Reporting** – results are collected into a Pandas table, summarized by
   count, charted with Matplotlib, and saved as CSV.

## Example

```
Reference: ATGCTACCGT
Sample:    ATGCTACAGT
```

Output:
```
Position  Reference Base  Sample Base  Mutation Type
8         C               A            Substitution
```

## Testing

The tool has been tested against:
- Identical sequences (no mutations)
- Single substitutions
- Single insertions
- Single deletions
- Multiple mixed mutations in one sequence
- Invalid input (non-ATGC characters)
