import streamlit as st
import plotly.express as px

from src.anomaly_detection.anomaly_detector import AnomalyDetector
from src.ui.layout import page_header, ai_insight, page_footer

st.set_page_config(
    page_title="AI Anomaly Detection",
    page_icon="🚨",
    layout="wide"
)

page_header(
    "🚨 AI Anomaly Detection",
    "Automatically detect unusual patterns and anomalies in business data."
)

# --------------------------------------------------
# CHECK DATASET
# --------------------------------------------------

if "dataset" not in st.session_state:

    st.warning("⚠ Please upload a dataset first.")

    st.stop()

df = st.session_state["dataset"]

st.success("✅ Dataset Loaded Successfully")

# --------------------------------------------------
# DATASET OVERVIEW
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
# RUN ANOMALY DETECTION
# --------------------------------------------------

detector = AnomalyDetector()

with st.spinner("🔍 Detecting anomalies..."):

    result = detector.detect(df)
    with st.spinner("Detecting anomalies..."):

        result = detector.detect(df)

if result is None:

    st.error("❌ Dataset has no numeric columns.")

    st.stop()

st.success("✅ Anomaly Detection Completed Successfully!")

# --------------------------------------------------
# PREVIEW
# --------------------------------------------------

with st.expander("📋 Preview Detection Results", expanded=True):

    st.dataframe(
        result.head(),
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# ANOMALY SUMMARY
# --------------------------------------------------

normal = len(
    result[result["Anomaly"] == "Normal"]
)

anomalies = len(
    result[result["Anomaly"] == "Anomaly"]
)

total = len(result)

percentage = round(
    (anomalies / total) * 100,
    2
)

st.subheader("📊 Anomaly Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Records",
        total
    )

with c2:
    st.metric(
        "Normal Records",
        normal
    )

with c3:
    st.metric(
        "Anomalies",
        anomalies
    )

with c4:
    st.metric(
        "Anomaly %",
        f"{percentage}%"
    )

st.divider()

# --------------------------------------------------
# DETECTED ANOMALIES
# --------------------------------------------------

st.subheader("🚨 Detected Anomalies")

anomaly_df = result[
    result["Anomaly"] == "Anomaly"
]

if len(anomaly_df) > 0:

    with st.expander(
        "📋 View Anomaly Records",
        expanded=True
    ):

        st.dataframe(
            anomaly_df,
            use_container_width=True
        )

else:

    st.success("✅ No anomalies detected.")

st.divider()

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

st.subheader("📈 Anomaly Distribution")

fig = px.pie(

    result,

    names="Anomaly",

    title="Normal vs Anomaly Records",

    hole=0.45

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

if len(anomaly_df) > 0:

    st.subheader("⬇ Export Report")

    csv = anomaly_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        "📥 Download Anomaly Report",

        csv,

        "anomaly_report.csv",

        "text/csv"

    )

st.divider()

# --------------------------------------------------
# BUSINESS INTERPRETATION
# --------------------------------------------------

st.subheader("🤖 AI Interpretation")

if anomalies == 0:

    st.success(
        "No abnormal records were detected. The dataset appears to be consistent."
    )

elif percentage < 5:

    st.info(
        "Only a small percentage of records are unusual. Review them before making business decisions."
    )

elif percentage < 15:

    st.warning(
        "A moderate number of anomalies were detected. Investigate potential operational or data quality issues."
    )

else:

    st.error(
        "A high anomaly rate was detected. Immediate investigation is recommended."
    )

ai_insight(
    "AI Anomaly Detection identifies unusual records that may indicate fraud, operational issues, data quality problems, or unexpected business events."
)

page_footer()