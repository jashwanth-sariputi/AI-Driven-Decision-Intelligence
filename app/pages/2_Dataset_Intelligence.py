import streamlit as st

from src.ui.layout import (
    page_header,
    ai_insight,
    page_footer
)

from src.dataset_intelligence.dataset_detector import (
    DatasetDetector
)

from src.dataset_intelligence.column_mapper import (
    ColumnMapper
)

from src.dataset_intelligence.recommendation_engine import (
    RecommendationEngine
)

from src.dataset_intelligence.quality_engine import (
    QualityEngine
)

from src.dataset_intelligence.insight_engine import (
    InsightEngine
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Dataset Intelligence",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

page_header(
    "🔍 Dataset Intelligence",
    "Analyze dataset quality, structure, compatibility and business opportunities."
)


# ============================================================
# CHECK DATASET
# ============================================================

if "dataset" not in st.session_state:

    st.warning(
        "📂 No dataset has been uploaded yet."
    )

    st.info(
        "Please go to **Upload Dataset** and upload your CSV or Excel file first."
    )

    st.stop()


# ============================================================
# LOAD DATASET
# ============================================================

df = st.session_state["dataset"]

filename = st.session_state.get(
    "filename",
    "Uploaded Dataset"
)


# ============================================================
# DATASET LOADED
# ============================================================

st.success(
    f"✅ Dataset Loaded: {filename}"
)


# ============================================================
# BASIC VALIDATION
# ============================================================

if df is None or df.empty:

    st.error(
        "❌ The dataset is empty or unavailable."
    )

    st.info(
        "Please return to Upload Dataset and upload the file again."
    )

    st.stop()


# ============================================================
# DATASET OVERVIEW
# ============================================================

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


# ============================================================
# ANALYSIS
# ============================================================

try:

    with st.spinner(
        "🧠 Nex Decision AI is analyzing your dataset..."
    ):

        # ----------------------------------------------------
        # DATASET DETECTOR
        # ----------------------------------------------------

        detector = DatasetDetector(df)

        report = detector.analyze_dataset()

        dataset_type, confidence = (
            detector.detect_dataset_type()
        )

        compatibility, reason = (
            detector.check_compatibility()
        )


        # ----------------------------------------------------
        # COLUMN MAPPER
        # ----------------------------------------------------

        mapper = ColumnMapper(
            df.columns
        )

        mapped_columns = (
            mapper.map_columns()
        )


        # ----------------------------------------------------
        # RECOMMENDATION ENGINE
        # ----------------------------------------------------

        recommendation_engine = (
            RecommendationEngine(
                dataset_type
            )
        )

        recommendations = (
            recommendation_engine.recommend()
        )


        # ----------------------------------------------------
        # QUALITY ENGINE
        # ----------------------------------------------------

        quality_engine = QualityEngine(
            df
        )

        quality_report = (
            quality_engine.generate_quality_report()
        )


        # ----------------------------------------------------
        # INSIGHT ENGINE
        # ----------------------------------------------------

        insight_engine = InsightEngine(
            dataset_type,
            quality_report,
            compatibility
        )

        insights = (
            insight_engine.generate_insights()
        )


    st.success(
        "✅ Dataset analysis completed successfully."
    )


except Exception:

    st.error(
        """
        ❌ Nex Decision AI could not complete the dataset analysis.

        This usually happens when the uploaded dataset has an
        unusual structure or unsupported columns.

        Your dataset is still safely stored.

        You can continue using the other features of the platform.
        """
    )

    st.stop()


# ============================================================
# DATASET ANALYSIS
# ============================================================

st.subheader("📋 Dataset Analysis")


with st.expander(
    "View Dataset Analysis",
    expanded=True
):

    if isinstance(report, dict):

        st.json(report)

    else:

        st.write(report)


st.divider()


# ============================================================
# DATASET TYPE
# ============================================================

st.subheader("📂 Dataset Type")


c1, c2 = st.columns(2)


with c1:

    st.info(
        f"Detected Type: **{dataset_type}**"
    )


with c2:

    st.metric(
        "Confidence",
        f"{confidence}%"
    )


st.divider()


# ============================================================
# COMPATIBILITY
# ============================================================

st.subheader("✅ Dataset Compatibility")


if str(compatibility).lower() == "compatible":

    st.success(
        "✅ Dataset is compatible with Nex Decision AI."
    )

else:

    st.warning(
        f"⚠️ {compatibility}"
    )


st.info(
    reason
)


st.divider()


# ============================================================
# COLUMN MAPPING
# ============================================================

st.subheader(
    "🗂 Universal Column Mapping"
)


with st.expander(
    "View Detected Column Mapping"
):

    if isinstance(
        mapped_columns,
        dict
    ):

        for key, value in mapped_columns.items():

            st.write(
                f"**{key}:** {value}"
            )

    else:

        st.write(
            mapped_columns
        )


st.divider()


# ============================================================
# RECOMMENDED AI SOLUTIONS
# ============================================================

st.subheader(
    "🤖 Recommended AI Solutions"
)


if recommendations:

    for item in recommendations:

        st.success(
            f"💡 {item}"
        )

else:

    st.info(
        "No specific AI recommendations were generated."
    )


st.divider()


# ============================================================
# DATA QUALITY
# ============================================================

st.subheader(
    "📈 Data Quality"
)


try:

    quality_score = quality_report.get(
        "Quality Score",
        "Unknown"
    )

    grade = quality_report.get(
        "Grade",
        "Unknown"
    )

    rows = quality_report.get(
        "Rows",
        len(df)
    )

    columns = quality_report.get(
        "Columns",
        len(df.columns)
    )


except Exception:

    quality_score = "Unknown"
    grade = "Unknown"
    rows = len(df)
    columns = len(df.columns)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Quality Score",
        quality_score
    )


with c2:

    st.metric(
        "Grade",
        grade
    )


with c3:

    st.metric(
        "Rows",
        f"{rows:,}"
    )


with c4:

    st.metric(
        "Columns",
        columns
    )


with st.expander(
    "📋 View Complete Quality Report"
):

    if isinstance(
        quality_report,
        dict
    ):

        st.json(
            quality_report
        )

    else:

        st.write(
            quality_report
        )


st.divider()


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.subheader(
    "💡 AI Business Insights"
)


if insights:

    for insight in insights:

        st.info(
            f"💡 {insight}"
        )

else:

    st.info(
        "No additional business insights were generated."
    )


st.divider()


# ============================================================
# DATASET PREVIEW
# ============================================================

st.subheader(
    "📋 Dataset Preview"
)


with st.expander(
    "View Uploaded Dataset"
):

    st.dataframe(
        df.head(20),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# AI INSIGHT
# ============================================================

ai_insight(
    "Understanding your dataset before machine learning helps improve model selection, data quality and business decision-making."
)


# ============================================================
# FOOTER
# ============================================================

page_footer()