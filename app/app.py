import streamlit as st
import pandas as pd

from src.dataset_intelligence.dataset_detector import DatasetDetector
from src.dataset_intelligence.column_mapper import ColumnMapper
from src.dataset_intelligence.recommendation_engine import RecommendationEngine
from src.dataset_intelligence.quality_engine import QualityEngine
from src.dataset_intelligence.insight_engine import InsightEngine
from src.database.database import Database

from src.reporting.report_generator import ExecutiveReportGenerator
from src.reporting.pdf_report import PDFReportGenerator

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="AI-Driven Decision Intelligence Platform",
    page_icon="🤖",
    layout="wide"
)
st.sidebar.title("🚀 AI-Driven Decision Intelligence")

st.sidebar.markdown("---")

st.sidebar.success("Enterprise AI Analytics Platform")

st.sidebar.markdown("---")

if "username" in st.session_state:
    st.sidebar.success(
        f"👤 {st.session_state['username']}"
    )

if "filename" in st.session_state:
    st.sidebar.info(
        f"📂 {st.session_state['filename']}"
    )

st.sidebar.markdown("---")

st.sidebar.success("🟢 AI Engine Online")
# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🤖 AI-Driven Decision Intelligence Platform")
st.caption("Transforming Business Data into Intelligent Decisions")

st.markdown("---")

# ---------------------------------------------------
# DATASET UPLOAD
# ---------------------------------------------------

st.header("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

# ---------------------------------------------------
# PROCESS DATASET
# ---------------------------------------------------

if uploaded_file is not None:

    # Read Dataset
    df = pd.read_csv(uploaded_file)
   

    # Store dataset for other pages
    st.session_state["dataset"] = df
    st.session_state["uploaded_filename"] = uploaded_file.name

    # Dataset Detection
    detector = DatasetDetector(df)

    report = detector.analyze_dataset()
    dataset_type, confidence = detector.detect_dataset_type()
    compatibility, reason = detector.check_compatibility()
    # Save upload history
    database = Database()

    if "last_uploaded_file" not in st.session_state:
        st.session_state["last_uploaded_file"] = ""

    if st.session_state["last_uploaded_file"] != uploaded_file.name:

        database.save_upload(
            uploaded_file.name,
            len(df),
            len(df.columns),
            dataset_type
        )

        st.session_state["last_uploaded_file"] = uploaded_file.name

        st.success("✅ Upload saved to history.")

    # Column Mapping
    mapper = ColumnMapper(df.columns)
    mapped_columns = mapper.map_columns()

    # Recommendation Engine
    recommendation_engine = RecommendationEngine(dataset_type)
    recommendations = recommendation_engine.recommend()

    # Quality Engine
    quality_engine = QualityEngine(df)
    quality_report = quality_engine.generate_quality_report()

    # Insight Engine
    insight_engine = InsightEngine(
        dataset_type,
        quality_report,
        compatibility
    )

    insights = insight_engine.generate_insights()

    # Executive Report
    report_generator = ExecutiveReportGenerator(
        dataset_type,
        quality_report,
        compatibility,
        recommendations,
        insights
    )

    executive_report = report_generator.generate_report()

    # ---------------------------------------------------
    # Dataset Analysis
    # ---------------------------------------------------

    st.subheader("📊 Dataset Analysis Report")
    st.write(report)

    # Dataset Type

    st.subheader("📂 Dataset Type")
    st.success(dataset_type)
    st.metric("Confidence", f"{confidence}%")

    # Compatibility

    st.subheader("✅ Compatibility Check")

    if compatibility == "Compatible":
        st.success(compatibility)
    else:
        st.error(compatibility)

    st.info(reason)

    # Dataset Preview

    st.success("Dataset uploaded successfully!")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Dataset Information

    st.subheader("Dataset Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", report["Rows"])

    with col2:
        st.metric("Columns", report["Columns"])

    with col3:
        st.metric("Missing Values", report["Missing Values"])

    st.subheader("Column Names")
    st.write(list(df.columns))

    # Column Mapping

    st.subheader("🗂 Universal Column Mapping")
    st.write(mapped_columns)

    # Recommendations

    st.subheader("🤖 Recommended AI Solutions")

    for recommendation in recommendations:
        st.success(recommendation)

    # Data Quality

    st.subheader("📈 AI Data Quality Report")

    q1, q2 = st.columns(2)

    with q1:
        st.metric("Quality Score", quality_report["Quality Score"])
        st.metric("Grade", quality_report["Grade"])
        st.metric("Missing Values", quality_report["Missing Values"])

    with q2:
        st.metric("Rows", quality_report["Rows"])
        st.metric("Columns", quality_report["Columns"])
        st.metric("Duplicate Rows", quality_report["Duplicate Rows"])

    st.write("### Quality Details")
    st.write(quality_report)

    # Business Insights

    st.subheader("💡 AI Business Insights")

    for insight in insights:
        st.info(insight)

    # Executive Report

    st.subheader("📄 AI Executive Business Report")

    st.text_area(
        "Executive Report",
        executive_report,
        height=400
    )

    pdf = PDFReportGenerator()

    pdf.generate(
        executive_report,
        "Executive_Report.pdf"
    )

    with open("Executive_Report.pdf", "rb") as file:

        st.download_button(
            label="📥 Download Executive PDF Report",
            data=file,
            file_name="Executive_Report.pdf",
            mime="application/pdf"
        )

# ---------------------------------------------------
# ABOUT
# ---------------------------------------------------

st.markdown("---")

st.header("📌 About the Platform")

st.write("""
This platform helps organizations automatically analyze business datasets,
predict customer churn,
identify business risks,
generate AI-powered recommendations,
evaluate dataset quality,
and provide intelligent business insights.
""")

st.markdown("---")

st.success("Platform Initialized Successfully ✅")