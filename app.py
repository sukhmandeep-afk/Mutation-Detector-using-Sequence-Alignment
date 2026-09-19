import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import report
from align import align_sequences
from detector import detect_mutations

# 1. Page Configuration
st.set_page_config(
    page_title="DNA Mutation Detector",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Styling (Hides default headers, adds dark gradient background and glass cards)
custom_css = """
<style>
/* Hide Streamlit header, footer, and menu */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stAppHeader {display: none;}

/* Dark gradient background */
.stApp {
    background: linear-gradient(-45deg, #090d16, #111827, #1e1b4b, #0f172a) !important;
    background-size: 400% 400% !important;
    animation: gradientAnimation 12s ease infinite !important;
}

@keyframes gradientAnimation {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Metric card styling */
.metric-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: #6366f1;
    box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.25);
}

.metric-card h3 {
    margin: 0;
    font-size: 13px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-card p {
    margin: 8px 0 0 0;
    font-size: 26px;
    font-weight: 700;
    color: #38bdf8;
}

/* Header Banner */
.hero-header {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(16px);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 25px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
}

.hero-header h1 {
    color: #f8fafc;
    font-weight: 800;
    margin-bottom: 6px;
}

.hero-header p {
    color: #cbd5e1;
    font-size: 15px;
    margin: 0;
}

/* Alignment display box */
.alignment-box {
    background-color: rgba(2, 6, 23, 0.85);
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 15px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 14px;
    color: #38bdf8;
    white-space: pre-wrap;
    word-break: break-all;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Main Header Section
st.markdown("""
<div class="hero-header">
    <h1>🧬 DNA Mutation Detection Platform</h1>
    <p>Automated sequence alignment and variant calling pipeline for genomic analysis.</p>
</div>
""", unsafe_allow_html=True)

# 4. Input Sidebar
st.sidebar.header("⚙️ Sequence Input")
input_option = st.sidebar.radio("Select Input Source:", ["Manual Input", "Upload FASTA Files"])

seq1, seq2 = "", ""

if input_option == "Manual Input":
    st.sidebar.subheader("Enter Sequences")
    seq1 = st.sidebar.text_area("Reference Sequence (DNA):", "ATCGGACTACGA", height=100).upper().strip()
    seq2 = st.sidebar.text_area("Sample Sequence (DNA):", "ATCGAACTACGA", height=100).upper().strip()
else:
    st.sidebar.subheader("Upload FASTA Files")
    file1 = st.sidebar.file_uploader("Reference FASTA (.fasta / .txt)", type=["fasta", "txt", "fa"])
    file2 = st.sidebar.file_uploader("Sample FASTA (.fasta / .txt)", type=["fasta", "txt", "fa"])

    if file1 and file2:
        seq1 = "".join([line.decode("utf-8").strip() for line in file1 if not line.decode("utf-8").startswith(">")]).upper()
        seq2 = "".join([line.decode("utf-8").strip() for line in file2 if not line.decode("utf-8").startswith(">")]).upper()

# 5. Summary Helper (Extracts string attributes from custom objects safely)
def generate_summary(mutations):
    summary = {"Substitution": 0, "Insertion": 0, "Deletion": 0}
    for m in mutations:
        raw_val = None
        # Handle custom class objects, dictionaries, lists, or strings
        if hasattr(m, "type"):
            raw_val = getattr(m, "type")
        elif hasattr(m, "mutation_type"):
            raw_val = getattr(m, "mutation_type")
        elif isinstance(m, dict):
            raw_val = m.get("type") or m.get("Type") or m.get("mutation_type")
        elif isinstance(m, (list, tuple)) and len(m) > 0:
            raw_val = m[0]
        else:
            raw_val = str(m)

        # Convert to string to avoid unhashable type errors
        m_str = str(raw_val).lower() if raw_val is not None else ""

        if "sub" in m_str:
            summary["Substitution"] += 1
        elif "ins" in m_str:
            summary["Insertion"] += 1
        elif "del" in m_str:
            summary["Deletion"] += 1

    return summary

# 6. Pipeline Execution
run_analysis = st.sidebar.button("🔬 Run Pipeline", use_container_width=True, type="primary")

if run_analysis:
    if not seq1 or not seq2:
        st.error("⚠️ Please provide valid sequences in both input fields before running analysis.")
    else:
        with st.spinner("Processing alignment and calculating variants..."):
            alignment_result = align_sequences(seq1, seq2)
            if isinstance(alignment_result, tuple) and len(alignment_result) == 3:
                aligned_ref, aligned_sam, align_score = alignment_result
            else:
                aligned_ref, aligned_sam = alignment_result[0], alignment_result[1]
                align_score = "N/A"

            mutations = detect_mutations(aligned_ref, aligned_sam)
            summary = generate_summary(mutations)

        st.success("✅ Analysis Completed Successfully!")

        # Metric Summary Row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f'<div class="metric-card"><h3>Alignment Score</h3><p>{align_score}</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><h3>Substitutions</h3><p>{summary.get("Substitution", 0)}</p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><h3>Insertions</h3><p>{summary.get("Insertion", 0)}</p></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><h3>Deletions</h3><p>{summary.get("Deletion", 0)}</p></div>', unsafe_allow_html=True)
        with col5:
            st.markdown(f'<div class="metric-card"><h3>Total Variants</h3><p>{len(mutations)}</p></div>', unsafe_allow_html=True)

        st.write("")
        st.write("")

        # Presentation Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📜 Alignment View", "📊 Variant Table", "📈 Distribution Chart", "💾 Export Results"])

        with tab1:
            st.subheader("Global Sequence Alignment Output")
            st.markdown(f"""
            <div class="alignment-box">
<b>Ref:</b>  {aligned_ref}
<b>Sam:</b>  {aligned_sam}
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.subheader("Detected Mutations (1-Based Reference Indexing)")
            if mutations:
                try:
                    df = pd.DataFrame(mutations)
                except Exception:
                    df = pd.DataFrame([vars(m) if hasattr(m, '__dict__') else str(m) for m in mutations])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No mutations detected between reference and sample sequences.")

        with tab3:
            st.subheader("Mutation Breakdown")
            if mutations:
                if hasattr(report, 'plot_mutation_distribution'):
                    try:
                        fig = report.plot_mutation_distribution(summary)
                        st.pyplot(fig)
                    except Exception:
                        fig, ax = plt.subplots(figsize=(6, 3))
                        ax.bar(summary.keys(), summary.values(), color=['#38bdf8', '#818cf8', '#f43f5e'])
                        ax.set_ylabel("Count")
                        st.pyplot(fig)
                else:
                    fig, ax = plt.subplots(figsize=(6, 3))
                    ax.bar(summary.keys(), summary.values(), color=['#38bdf8', '#818cf8', '#f43f5e'])
                    ax.set_ylabel("Count")
                    st.pyplot(fig)
            else:
                st.info("No distribution chart available (Zero variants detected).")

        with tab4:
            st.subheader("Download Reports")
            if mutations:
                try:
                    df = pd.DataFrame(mutations)
                except Exception:
                    df = pd.DataFrame([vars(m) if hasattr(m, '__dict__') else str(m) for m in mutations])
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download CSV Mutation Report",
                    data=csv,
                    file_name="mutation_report.csv",
                    mime="text/csv",
                    type="primary"
                )
            else:
                st.info("No report data available to download.")

else:
    st.info("👈 Use the sidebar panel to enter DNA sequences or upload FASTA files, then click **Run Pipeline**.")
