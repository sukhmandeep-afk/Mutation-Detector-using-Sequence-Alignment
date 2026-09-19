import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from align import align_sequences
from detector import detect_mutations
from report import generate_summary, save_csv_report, plot_mutation_distribution

# 1. Page Configuration
st.set_page_config(
    page_title="DNA Mutation Detector",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS styling (Hides menus, adds custom background, cards, and UI polish)
custom_css = """
<style>
/* Hide default Streamlit header, footer, and top menu */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stAppHeader {display: none;}

/* Modern gradient background with abstract subtle animation */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    color: #f8fafc;
    font-family: 'Inter', sans-serif;
}

/* Container Glassmorphism effect */
div[data-testid="stExpander"], div[data-testid="stForm"], .css-1r6slb0, .stMarkdownContainer {
    border-radius: 10px;
}

/* Custom Card Layouts for Metric summaries */
.metric-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-3px);
    border-color: #6366f1;
}

.metric-card h3 {
    margin: 0;
    font-size: 14px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.metric-card p {
    margin: 8px 0 0 0;
    font-size: 28px;
    font-weight: 700;
    color: #38bdf8;
}

/* Hero Section Branding */
.hero-header {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 25px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

.hero-header h1 {
    color: #f8fafc;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-header p {
    color: #cbd5e1;
    font-size: 16px;
    margin: 0;
}

/* Sequence alignment box styling */
.alignment-box {
    background-color: #020617;
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
    <p>Automated global sequence alignment (Needleman-Wunsch) and variant identification pipeline for genetic analysis.</p>
</div>
""", unsafe_allow_html=True)

# 4. Input Controls Section
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

# 5. Pipeline Execution Trigger
run_analysis = st.sidebar.button("🔬 Run Pipeline", use_container_width=True, type="primary")

if run_analysis:
    if not seq1 or not seq2:
        st.error("⚠️ Please provide valid sequences in both input fields before running analysis.")
    else:
        with st.spinner("Processing alignment and calculating variants..."):
            # Execute backend modules without changing any logic
            aligned_ref, aligned_sam, align_score = align_sequences(seq1, seq2)
            mutations = detect_mutations(aligned_ref, aligned_sam)
            summary = generate_summary(mutations)

        st.success("✅ Analysis Completed Successfully!")

        # 6. Interactive Metric Dashboard
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f'<div class="metric-card"><h3>Alignment Score</h3><p>{align_score:.1f}</p></div>', unsafe_allow_html=True)
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

        # 7. Presentation Tabs for Results
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
                df = pd.DataFrame(mutations)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No mutations detected between reference and sample sequences.")

        with tab3:
            st.subheader("Mutation Breakdown")
            if mutations:
                fig = plot_mutation_distribution(summary)
                st.pyplot(fig)
            else:
                st.info("No distribution chart available (Zero variants detected).")

        with tab4:
            st.subheader("Download Reports")
            if mutations:
                df = pd.DataFrame(mutations)
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
