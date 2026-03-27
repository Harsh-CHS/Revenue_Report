import os
from datetime import datetime
import streamlit as st 
from parser import build_portfolio_data
from pdf_builder import build_portfolio_pdf

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

st.set_page_config(
    page_title="TownePlace Portfolio Generator",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
/* ===== Base ===== */
.stApp {
    background: #f4f7fb;
}

.block-container {
    max-width: 1150px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* Hide top decoration spacing issues */
header[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* ===== Hero ===== */
.hero {
    background: linear-gradient(135deg, #123b68 0%, #1d4f86 100%);
    border-radius: 20px;
    padding: 28px 30px;
    color: white;
    box-shadow: 0 8px 24px rgba(18, 59, 104, 0.18);
    margin-bottom: 20px;
}

.hero h1 {
    margin: 0 0 10px 0;
    font-size: 2rem;
    font-weight: 800;
    color: white;
}

.hero p {
    margin: 0;
    font-size: 1rem;
    color: #e9f1fb;
    line-height: 1.6;
}

.hero-badge {
    display: inline-block;
    margin-top: 14px;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.22);
    color: white;
    font-size: 0.9rem;
    font-weight: 600;
}

/* ===== Section cards ===== */
.section-card {
    background: white;
    border: 1px solid #dbe4f0;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 4px 14px rgba(28, 55, 90, 0.06);
    min-height: 100px;
}

.section-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #17324d;
    margin-bottom: 8px;
}

.section-text {
    color: #4f647a;
    font-size: 0.96rem;
    line-height: 1.55;
    margin-bottom: 14px;
}

/* ===== File uploader: keep it native but readable ===== */
[data-testid="stFileUploader"] {
    background: #f8fbff;
    border: 1.5px dashed #a9bfd8;
    border-radius: 14px;
    padding: 10px;
}

[data-testid="stFileUploader"] * {
    color: #17324d !important;
}

section[data-testid="stFileUploaderDropzone"] {
    background: #f8fbff !important;
    border: 1.5px dashed #a9bfd8 !important;
    border-radius: 12px !important;
}

section[data-testid="stFileUploaderDropzone"] * {
    color: #17324d !important;
    fill: #17324d !important;
}

[data-testid="stFileUploaderFileName"] {
    color: #17324d !important;
    font-weight: 700 !important;
}

/* Labels */
label {
    color: #17324d !important;
    font-weight: 700 !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    width: 100%;
    border-radius: 12px;
    border: none;
    padding: 0.85rem 1rem;
    font-weight: 700;
    font-size: 1rem;
}

.stButton > button {
    background: linear-gradient(90deg, #2563eb 0%, #6d28d9 100%);
    color: white;
    box-shadow: 0 8px 18px rgba(37, 99, 235, 0.22);
}

.stDownloadButton > button {
    background: linear-gradient(90deg, #0f766e 0%, #0ea5a4 100%);
    color: white;
    box-shadow: 0 8px 18px rgba(15, 118, 110, 0.18);
}

/* Info cards */
.stat-card {
    background: white;
    border: 1px solid #dbe4f0;
    border-radius: 16px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(28, 55, 90, 0.05);
}

.stat-label {
    color: #5f748a;
    font-size: 0.86rem;
    margin-bottom: 6px;
}

.stat-value {
    color: #17324d;
    font-size: 1.35rem;
    font-weight: 800;
}

/* Alert readability */
[data-testid="stAlert"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>H2H KPIs- Hotel Daily Report Generator</h1>
    <p>
        Upload the Tehachapi and Ridgecrest TXT revenue reports to generate the combined
        portfolio PDF in the target layout.
    </p>
    <div class="hero-badge">Output file name automatically adds today’s running date</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="section-card">
        <div class="section-title">Tehachapi Source File</div>
        <div class="section-text">
            Upload the TXT revenue report for <b>TPS Tehachapi</b>.
        </div>
    """, unsafe_allow_html=True)

    file1 = st.file_uploader(
        "Upload Tehachapi TXT",
        type=["txt"],
        key="tehachapi_file"
    )

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="section-card">
        <div class="section-title">Ridgecrest Source File</div>
        <div class="section-text">
            Upload the TXT revenue report for <b>TPS Ridgecrest</b>.
        </div>
    """, unsafe_allow_html=True)

    file2 = st.file_uploader(
        "Upload Ridgecrest TXT",
        type=["txt"],
        key="ridgecrest_file"
    )

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
generate = st.button("Generate Portfolio PDF")

if file1 and file2 and generate:
    try:
        portfolio_data = build_portfolio_data(file1.read(), file2.read())

        today_str = datetime.today().strftime("%Y-%m-%d")
        filename = f"TownePlace_Suites_Portfolio_{today_str}.pdf"
        output_path = os.path.join(OUTPUT_DIR, filename)

        build_portfolio_pdf(portfolio_data, output_path)

        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-label">Report Date</div>
                <div class="stat-value">TXT Based</div>
            </div>
            """, unsafe_allow_html=True)
        with s2:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-label">Input Files</div>
                <div class="stat-value">2</div>
            </div>
            """, unsafe_allow_html=True)
        with s3:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-label">Output</div>
                <div class="stat-value">1 PDF</div>
            </div>
            """, unsafe_allow_html=True)

        st.success("Portfolio PDF generated successfully.")

        with open(output_path, "rb") as f:
            st.download_button(
                label=f"Download {filename}",
                data=f,
                file_name=filename,
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Error: {str(e)}")