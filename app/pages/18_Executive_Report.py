import streamlit as st
from src.ui.layout import page_header, ai_insight, page_footer
from src.executive_reports.report_builder import ExecutiveReportBuilder

st.set_page_config(
    page_title="Executive Report",
    page_icon="📄",
    layout="wide"
)

page_header(
    "📄 Executive Report Generator",
    "Generate professional business reports for management and stakeholders."
)

# ------------------------------------------------
# Check Dataset
# ------------------------------------------------

if "dataset" not in st.session_state:

    st.warning("Please upload a dataset first.")

    st.stop()

df = st.session_state["dataset"]

# ------------------------------------------------
# Dataset Statistics
# ------------------------------------------------

rows = len(df)
columns = len(df.columns)
missing = int(df.isnull().sum().sum())
duplicates = int(df.duplicated().sum())

dataset_summary = {

    "Rows": rows,
    "Columns": columns,
    "Missing": missing,
    "Duplicates": duplicates

}

# ------------------------------------------------
# Business Health Score
# ------------------------------------------------

health = 100

health -= min(missing * 2, 30)

health -= min(duplicates * 2, 20)

health = max(0, health)

if health >= 90:
    grade = "🟢 Excellent"

elif health >= 75:
    grade = "🟡 Good"

elif health >= 60:
    grade = "🟠 Average"

else:
    grade = "🔴 Poor"

# ------------------------------------------------
# Dashboard
# ------------------------------------------------

st.subheader("📊 Executive Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Rows", rows)

with c2:
    st.metric("Columns", columns)

with c3:
    st.metric("Missing", missing)

with c4:
    st.metric("Duplicates", duplicates)

st.markdown("---")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Business Health Score",
        f"{health}/100"
    )

with c2:
    st.metric(
        "Overall Grade",
        grade
    )

st.markdown("---")

# ------------------------------------------------
# AI Summary
# ------------------------------------------------

st.subheader("🤖 AI Executive Summary")

st.info(f"""
The uploaded dataset contains **{rows:,} records** and **{columns} features**.

• Missing Values : **{missing}**

• Duplicate Rows : **{duplicates}**

• Overall Business Health Score : **{health}/100**

The dataset is suitable for advanced business analytics and AI model development.
""")

st.markdown("---")

# ------------------------------------------------
# AutoML Summary
# ------------------------------------------------

automl_result = """
Best Model : Refer AutoML Page

Problem Type : Automatically Detected

Performance : Highest Performing Saved Model
"""

st.subheader("🤖 AutoML Summary")

st.success(automl_result)

st.markdown("---")

# ------------------------------------------------
# Recommendations
# ------------------------------------------------

recommendations = [

    "Clean missing values before training models.",

    "Remove duplicate records.",

    "Use AutoML to compare algorithms.",

    "Monitor anomalies regularly.",

    "Generate business forecasts.",

    "Deploy the best-performing model."

]

st.subheader("💡 AI Recommendations")

for recommendation in recommendations:

    st.success(recommendation)

st.markdown("---")

# ------------------------------------------------
# Anomaly Summary
# ------------------------------------------------

anomaly_summary = """
Isolation Forest was used for anomaly detection.

Refer to the AI Anomaly Detection page
for complete anomaly analysis.
"""

st.subheader("🚨 Anomaly Detection Summary")

st.warning(anomaly_summary)

st.markdown("---")

# ------------------------------------------------
# Generate PDF
# ------------------------------------------------

builder = ExecutiveReportBuilder()

with st.spinner("📄 Generating Executive Report..."):

    # report generation code

    filename = builder.generate(

        filename="Executive_Report.pdf",

        dataset_summary=dataset_summary,

        health_score=health,

        automl_result=automl_result,

        recommendations=recommendations,

        anomaly_summary=anomaly_summary

    )

    st.success("✅ Executive Report Generated Successfully!")

    with open(filename, "rb") as file:

        st.download_button(

            "⬇ Download Executive Report",

            data=file,

            file_name="Executive_Report.pdf",

            mime="application/pdf"

        )

st.markdown("---")

ai_insight(
    "Executive reports summarize KPIs, AI findings, business health, predictions, anomalies, and strategic recommendations for decision-makers."
)

page_footer()