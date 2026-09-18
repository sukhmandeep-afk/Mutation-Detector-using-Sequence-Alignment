"""
app.py
------
Optional Streamlit web interface for the Mutation Detector.

Run with:
    streamlit run app.py

(Requires: pip install streamlit biopython pandas matplotlib)
"""

import streamlit as st
import matplotlib.pyplot as plt

from detector import validate_sequence, detect_mutations, read_fasta
from report import mutations_to_dataframe, summarize_mutations

st.set_page_config(page_title="Mutation Detector", page_icon="🧬", layout="centered")
# Hide Streamlit header, top-right menu, and GitHub links
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppHeader {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("🧬 Mutation Detector Using Sequencing Alignment")
st.write(
    "Compare a reference DNA sequence to a sample DNA sequence and automatically "
    "detect substitutions, insertions, and deletions."
)

st.subheader("1. Input Sequences")
input_mode = st.radio("Input method", ["Paste sequence text", "Upload FASTA files"], horizontal=True)

reference_seq = ""
sample_seq = ""

if input_mode == "Paste sequence text":
    col1, col2 = st.columns(2)
    with col1:
        reference_seq = st.text_area("Reference sequence", value="ATGCTACCGT", height=100)
    with col2:
        sample_seq = st.text_area("Sample sequence", value="ATGCTACAGT", height=100)
else:
    col1, col2 = st.columns(2)
    with col1:
        ref_file = st.file_uploader("Reference FASTA file", type=["fasta", "fa", "txt"])
        if ref_file:
            reference_seq = "".join(
                line.strip().upper()
                for line in ref_file.read().decode("utf-8").splitlines()
                if line and not line.startswith(">")
            )
    with col2:
        sample_file = st.file_uploader("Sample FASTA file", type=["fasta", "fa", "txt"])
        if sample_file:
            sample_seq = "".join(
                line.strip().upper()
                for line in sample_file.read().decode("utf-8").splitlines()
                if line and not line.startswith(">")
            )

if st.button("Detect Mutations", type="primary"):
    reference_seq = reference_seq.strip().upper()
    sample_seq = sample_seq.strip().upper()

    if not reference_seq or not sample_seq:
        st.error("Please provide both a reference and a sample sequence.")
    elif not validate_sequence(reference_seq):
        st.error("Reference sequence contains invalid characters. Only A, T, G, C are allowed.")
    elif not validate_sequence(sample_seq):
        st.error("Sample sequence contains invalid characters. Only A, T, G, C are allowed.")
    else:
        mutations, aligned_ref, aligned_sample = detect_mutations(reference_seq, sample_seq)
        df = mutations_to_dataframe(mutations)
        summary = summarize_mutations(mutations)

        st.subheader("2. Alignment")
        st.code(f"Reference: {aligned_ref}\nSample:    {aligned_sample}", language="text")

        st.subheader("3. Summary")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Mutations", summary["Total Mutations"])
        c2.metric("Substitutions", summary["Substitutions"])
        c3.metric("Insertions", summary["Insertions"])
        c4.metric("Deletions", summary["Deletions"])

        st.subheader("4. Mutation Table")
        if df.empty:
            st.success("No mutations detected. Sequences are identical.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.subheader("5. Mutation Chart")
            labels = ["Substitutions", "Insertions", "Deletions"]
            values = [summary["Substitutions"], summary["Insertions"], summary["Deletions"]]
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(labels, values, color=["#4C72B0", "#DD8452", "#55A868"])
            ax.set_ylabel("Count")
            ax.set_title("Mutation Types Detected")
            st.pyplot(fig)

            st.subheader("6. Download Report")
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download mutation_report.csv", csv_data, "mutation_report.csv", "text/csv")
