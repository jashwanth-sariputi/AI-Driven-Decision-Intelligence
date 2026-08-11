import streamlit as st
import pandas as pd

from src.ui.layout import page_header, ai_insight, page_footer


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📂",
    layout="wide"
)


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_dataset(file_bytes, filename):
    """
    Load CSV or Excel dataset safely.
    """

    try:
        if filename.lower().endswith(".csv"):
            from io import BytesIO
            return pd.read_csv(BytesIO(file_bytes))

        elif filename.lower().endswith(".xlsx"):
            from io import BytesIO
            return pd.read_excel(BytesIO(file_bytes))

        elif filename.lower().endswith(".xls"):
            from io import BytesIO
            return pd.read_excel(BytesIO(file_bytes))

        else:
            return None

    except Exception:
        return None


# ============================================================
# HEADER
# ============================================================

page_header(
    "📂 Upload Dataset",
    "Upload a business dataset to begin AI-powered business analytics."
)


# ============================================================
# INTRODUCTION
# ============================================================

st.markdown(
    """
    ### Upload your business dataset

    Nex Decision AI automatically analyzes your dataset and provides:

    - 📊 Dataset statistics
    - 🔍 Dataset type detection
    - 🧹 Data quality analysis
    - 🗂 Column intelligence
    - 🤖 AI solution recommendations
    - 💡 Business insights
    - 📈 Machine learning opportunities
    """
)


# ============================================================
# SUPPORTED FORMATS
# ============================================================

st.info(
    """
    **Supported formats**

    📄 CSV  
    📊 Excel (.xlsx / .xls)
    """
)


# ============================================================
# FILE UPLOADER
# ============================================================

uploaded_file = st.file_uploader(
    "Choose your dataset",
    type=["csv", "xlsx", "xls"],
    help="Upload a CSV or Excel business dataset."
)


# ============================================================
# PROCESS UPLOADED DATASET
# ============================================================

if uploaded_file is not None:

    try:

        with st.spinner("Reading and validating your dataset..."):

            file_bytes = uploaded_file.getvalue()

            df = load_dataset(
                file_bytes,
                uploaded_file.name
            )

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if df is None:

            st.error(
                "❌ We couldn't read this file. "
                "Please upload a valid CSV or Excel dataset."
            )

            st.stop()


        if df.empty:

            st.warning(
                "⚠️ The uploaded dataset is empty. "
                "Please upload a dataset containing data."
            )

            st.stop()


        # ----------------------------------------------------
        # STORE DATASET
        # ----------------------------------------------------

        st.session_state["dataset"] = df
        st.session_state["filename"] = uploaded_file.name


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        st.success(
            f"✅ Dataset '{uploaded_file.name}' uploaded successfully."
        )


        # ====================================================
        # DATASET OVERVIEW
        # ====================================================

        st.subheader("📊 Dataset Overview")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "📄 Rows",
                f"{len(df):,}"
            )

        with c2:
            st.metric(
                "📊 Columns",
                len(df.columns)
            )

        with c3:
            st.metric(
                "⚠ Missing Values",
                f"{int(df.isnull().sum().sum()):,}"
            )

        with c4:
            st.metric(
                "🔁 Duplicate Rows",
                f"{int(df.duplicated().sum()):,}"
            )


        st.divider()


        # ====================================================
        # DATASET PREVIEW
        # ====================================================

        st.subheader("📋 Dataset Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True,
            hide_index=True
        )


        st.divider()


        # ====================================================
        # DATA TYPES
        # ====================================================

        st.subheader("🔎 Dataset Structure")

        c1, c2, c3 = st.columns(3)

        with c1:
            numeric_columns = len(
                df.select_dtypes(
                    include="number"
                ).columns
            )

            st.metric(
                "🔢 Numeric Columns",
                numeric_columns
            )

        with c2:
            categorical_columns = len(
                df.select_dtypes(
                    include=["object", "category"]
                ).columns
            )

            st.metric(
                "🔤 Categorical Columns",
                categorical_columns
            )

        with c3:
            datetime_columns = len(
                df.select_dtypes(
                    include=["datetime"]
                ).columns
            )

            st.metric(
                "📅 Date Columns",
                datetime_columns
            )


        # ====================================================
        # DATASET INFORMATION
        # ====================================================

        with st.expander(
            "📋 View Dataset Information"
        ):

            st.write(
                "### Column Names"
            )

            st.write(
                list(df.columns)
            )

            st.write(
                "### Data Types"
            )

            st.dataframe(
                pd.DataFrame({
                    "Column": df.columns,
                    "Data Type": [
                        str(dtype)
                        for dtype in df.dtypes
                    ]
                }),
                use_container_width=True,
                hide_index=True
            )


        # ====================================================
        # NEXT STEP
        # ====================================================

        st.success(
            "🚀 Your dataset is ready for AI analysis."
        )

        st.info(
            "Go to **Dataset Intelligence** from the sidebar "
            "to analyze your dataset."
        )


    except Exception:

        st.error(
            """
            ❌ We couldn't process this dataset.

            Please check that:

            • The file is a valid CSV or Excel file  
            • The file is not corrupted  
            • The dataset contains tabular data  

            Then try uploading it again.
            """
        )


# ============================================================
# AI INSIGHT
# ============================================================

ai_insight(
    "Clean and well-structured business data helps Nex Decision AI generate more reliable insights and predictions."
)


# ============================================================
# FOOTER
# ============================================================

page_footer()