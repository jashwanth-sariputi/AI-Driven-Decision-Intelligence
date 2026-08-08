import streamlit as st
from src.ui.layout import page_header, ai_insight, page_footer
from src.business_copilot.copilot_engine import BusinessCopilot

st.set_page_config(
    page_title="AI Business Copilot",
    page_icon="🤖",
    layout="wide"
)

page_header(
    "🤖 AI Business Copilot",
    "Your Intelligent Business Decision Assistant"
)

# =====================================================
# CHECK DATASET
# =====================================================

if "dataset" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state["dataset"]

copilot = BusinessCopilot(df)

summary = copilot.executive_summary()
score = copilot.business_score()

# =====================================================
# KPI DASHBOARD
# =====================================================

st.subheader("📊 Executive Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Rows", summary["Rows"])

with c2:
    st.metric("Columns", summary["Columns"])

with c3:
    st.metric("Missing", summary["Missing"])

with c4:
    st.metric("Duplicates", summary["Duplicates"])

st.markdown("---")

# =====================================================
# BUSINESS HEALTH
# =====================================================

st.subheader("💚 Business Health Score")

st.progress(score / 100)

if score >= 90:
    st.success(f"Excellent Dataset ({score}/100)")
elif score >= 75:
    st.info(f"Good Dataset ({score}/100)")
elif score >= 60:
    st.warning(f"Average Dataset ({score}/100)")
else:
    st.error(f"Poor Dataset ({score}/100)")

st.markdown("---")

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.subheader("📄 Executive Summary")

st.info(f"""
Dataset contains **{summary['Rows']:,} rows** and **{summary['Columns']} columns**.

Missing Values : **{summary['Missing']}**

Duplicate Rows : **{summary['Duplicates']}**

Business Health Score : **{score}/100**
""")

st.markdown("---")

# =====================================================
# AI RECOMMENDATIONS
# =====================================================

left, right = st.columns([2,1])

with left:

    st.subheader("🤖 AI Recommendations")

    for rec in copilot.recommendations():
        st.success(rec)

with right:

    st.subheader("⚡ Suggested Next Steps")

    st.info("✔ Analyze Dataset")

    st.info("✔ Train AutoML")

    st.info("✔ Generate Forecast")

    st.info("✔ Predict Business Outcomes")

    st.info("✔ Download Executive Report")

st.markdown("---")

# =====================================================
# BUSINESS RISK ANALYSIS
# =====================================================

st.subheader("🚨 Business Risk Analysis")

risks = []

if summary["Missing"] > 0:
    risks.append("Missing values may reduce prediction accuracy.")

if summary["Duplicates"] > 0:
    risks.append("Duplicate records may bias machine learning models.")

if len(df.columns) < 5:
    risks.append("Limited features may reduce business insights.")

if len(risks) == 0:

    st.success("No major business risks detected.")

else:

    for risk in risks:
        st.warning(risk)

st.markdown("---")

# =====================================================
# AI OPPORTUNITIES
# =====================================================

st.subheader("🚀 AI Opportunities")

opportunities = [

    "Forecast future business trends",

    "Predict customer behaviour",

    "Detect anomalies automatically",

    "Build executive dashboards",

    "Improve business decision making"

]

for item in opportunities:
    st.success(item)

st.markdown("---")

# =====================================================
# AI CHAT
# =====================================================

st.subheader("💬 Ask AI Business Copilot")

question = st.text_input(
    "Ask a business question..."
)

example_questions = [
    "Summarize this dataset",
    "What are the data quality issues?",
    "How ready is this dataset for machine learning?",
    "Give business recommendations",
    "What risks do you identify?"
]

selected = st.selectbox(
    "Or choose a sample question",
    [""] + example_questions
)

if selected:
    question = selected

if question:
    with st.spinner("Thinking..."):

        answer = copilot.ask(question)


    st.markdown("### 🤖 AI Response")

    if hasattr(answer, "shape"):

        st.dataframe(
            answer,
            use_container_width=True
        )

    elif isinstance(answer, list):

        for item in answer:
            st.success(item)

    elif isinstance(answer, tuple):

        st.write(answer)

    else:

        st.info(answer)

st.markdown("---")

ai_insight(
    "The AI Business Copilot helps executives understand data quality, identify business opportunities, assess risks, and make data-driven decisions before building machine learning models."
)

page_footer()