import streamlit as st
from src.ui.layout import page_header, ai_insight, page_footer

from src.dataset_intelligence.dataset_detector import DatasetDetector
from src.dataset_intelligence.column_mapper import ColumnMapper
from src.dataset_intelligence.recommendation_engine import RecommendationEngine
from src.dataset_intelligence.quality_engine import QualityEngine
from src.dataset_intelligence.insight_engine import InsightEngine

st.set_page_config(
    page_title="Dataset Intelligence",
    page_icon="🧠",
    layout="wide"
)

page_header(
    "🔍 Dataset Intelligence",
    "Analyze dataset quality, structure, and statistical insights."
)

# --------------------------------------------------
# Check Dataset
# --------------------------------------------------

if "dataset" not in st.session_state:

    st.warning("Please upload a dataset first.")

    st.stop()

df = st.session_state["dataset"]
filename = st.session_state["filename"]

st.success(f"✅ Dataset Loaded : {filename}")

# --------------------------------------------------
# Analyze Dataset
# --------------------------------------------------

with st.spinner("Analyzing dataset..."):

    detector = DatasetDetector(df)

    report = detector.analyze_dataset()

    dataset_type, confidence = detector.detect_dataset_type()

    compatibility, reason = detector.check_compatibility()

    mapper = ColumnMapper(df.columns)

    mapped_columns = mapper.map_columns()

    recommendation_engine = RecommendationEngine(dataset_type)

    recommendations = recommendation_engine.recommend()

    quality_engine = QualityEngine(df)

    quality_report = quality_engine.generate_quality_report()

    insight_engine = InsightEngine(
        dataset_type,
        quality_report,
        compatibility
    )

    insights = insight_engine.generate_insights()

st.success("✅ Dataset Analysis Completed Successfully!")

# --------------------------------------------------
# Dataset Overview
# --------------------------------------------------

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

# --------------------------------------------------
# Dataset Detection
# --------------------------------------------------

detector = DatasetDetector(df)

report = detector.analyze_dataset()

dataset_type, confidence = detector.detect_dataset_type()

compatibility, reason = detector.check_compatibility()

# --------------------------------------------------
# Column Mapping
# --------------------------------------------------

mapper = ColumnMapper(df.columns)

mapped_columns = mapper.map_columns()

# --------------------------------------------------
# Recommendation Engine
# --------------------------------------------------

recommendation_engine = RecommendationEngine(dataset_type)

recommendations = recommendation_engine.recommend()

# --------------------------------------------------
# Quality Engine
# --------------------------------------------------

quality_engine = QualityEngine(df)

quality_report = quality_engine.generate_quality_report()

# --------------------------------------------------
# Insight Engine
# --------------------------------------------------

insight_engine = InsightEngine(
    dataset_type,
    quality_report,
    compatibility
)

insights = insight_engine.generate_insights()

# --------------------------------------------------
# Dataset Analysis
# --------------------------------------------------

st.subheader("📊 Dataset Analysis")

with st.expander("📋 View Dataset Analysis", expanded=True):

    st.write(report)

st.divider()

# --------------------------------------------------
# Dataset Type
# --------------------------------------------------

st.subheader("📂 Dataset Type")

c1, c2 = st.columns(2)

with c1:
    st.success(dataset_type)

with c2:
    st.metric(
        "Confidence",
        f"{confidence}%"
    )

st.divider()

# --------------------------------------------------
# Compatibility
# --------------------------------------------------

st.subheader("✅ Compatibility")

if compatibility == "Compatible":

    st.success(compatibility)

else:

    st.error(compatibility)

st.info(reason)

st.divider()

# --------------------------------------------------
# Column Mapping
# --------------------------------------------------

st.subheader("🗂 Universal Column Mapping")

with st.expander("📋 View Column Mapping"):

    st.write(mapped_columns)

st.divider()

# --------------------------------------------------
# Recommendations
# --------------------------------------------------

st.subheader("🤖 Recommended AI Solutions")

for item in recommendations:

    st.success(item)

st.divider()

# --------------------------------------------------
# Quality Report
# --------------------------------------------------

st.subheader("📈 Data Quality")

c1, c2 = st.columns(2)

with c1:

    st.metric(
        "Quality Score",
        quality_report["Quality Score"]
    )

    st.metric(
        "Grade",
        quality_report["Grade"]
    )

with c2:

    st.metric(
        "Rows",
        quality_report["Rows"]
    )

    st.metric(
        "Columns",
        quality_report["Columns"]
    )

with st.expander("📋 View Complete Quality Report"):

    st.write(quality_report)

st.divider()

# --------------------------------------------------
# Business Insights
# --------------------------------------------------

st.subheader("💡 AI Business Insights")

for insight in insights:

    st.info(insight)

ai_insight(
    "Understanding your dataset before model training leads to better machine learning performance."
)

page_footer()