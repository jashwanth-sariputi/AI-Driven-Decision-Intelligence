import streamlit as st
from src.ui.layout import page_header, ai_insight, page_footer

import pandas as pd
@st.cache_data
def load_dataset(uploaded_file):
    return pd.read_csv(uploaded_file)

st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📂",
    layout="wide"
)

page_header(
    "📂 Upload Dataset",
    "Upload a CSV or Excel dataset to begin AI-powered business analytics."
)

st.markdown("""
Upload your business dataset to begin AI-powered analysis.

Supported formats:

- CSV ✅
- Excel (.xlsx) 🔜
- SQL Database 🔜
- API 🔜
""")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    with st.spinner("Uploading dataset..."):
        df = load_dataset(uploaded_file)

    st.session_state["dataset"] = df
    st.session_state["filename"] = uploaded_file.name

    st.success("✅ Dataset uploaded successfully!")

    st.success(
        f"Dataset '{uploaded_file.name}' stored successfully."
    )

    # ----------------------------------------
    # Dataset Overview
    # ----------------------------------------

    st.subheader("📊 Dataset Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("📄 Rows", len(df))

    with c2:
        st.metric("📊 Columns", len(df.columns))

    with c3:
        st.metric("⚠ Missing", int(df.isnull().sum().sum()))

    with c4:
        st.metric("🔁 Duplicates", int(df.duplicated().sum()))

    st.divider()

    # ----------------------------------------
    # Dataset Preview
    # ----------------------------------------

    with st.expander("📋 Preview Uploaded Dataset", expanded=True):

        st.dataframe(
            df.head(),
            use_container_width=True
        )

    st.divider()

    # ----------------------------------------
    # Dataset Shape
    # ----------------------------------------

    st.subheader("📐 Dataset Shape")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    st.info(
        "Navigate to the Dataset Intelligence page to analyze this dataset."
    )

ai_insight(
    "Supported formats include CSV and Excel. Ensure column names are clean and consistent for the best experience."
)

page_footer()