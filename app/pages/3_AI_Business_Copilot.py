import streamlit as st

from src.ui.layout import page_header, ai_insight, page_footer
from src.business_copilot.copilot_engine import BusinessCopilot


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Business Copilot",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

page_header(
    "🤖 AI Business Copilot",
    "Your intelligent business decision assistant"
)


# =========================================================
# CHECK DATASET
# =========================================================

if "dataset" not in st.session_state:

    st.warning(
        "📂 Please upload a dataset first."
    )

    st.info(
        "Go to **Upload Dataset** from the sidebar "
        "and upload your business dataset."
    )

    st.stop()


# =========================================================
# LOAD DATASET
# =========================================================

df = st.session_state["dataset"]

filename = st.session_state.get(
    "filename",
    "Uploaded Dataset"
)


# =========================================================
# INITIALIZE COPILOT
# =========================================================

try:

    copilot = BusinessCopilot(df)

    summary = copilot.executive_summary()

    score = copilot.business_score()

except Exception:

    st.error(
        "⚠️ The AI Business Copilot could not analyze "
        "this dataset."
    )

    st.info(
        "Please check the uploaded dataset and try again."
    )

    st.stop()


# =========================================================
# DATASET STATUS
# =========================================================

st.success(
    f"✅ Dataset loaded successfully: **{filename}**"
)

st.markdown("---")


# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

st.subheader("📊 Executive Overview")


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "📄 Rows",
        f"{summary['Rows']:,}"
    )


with c2:

    st.metric(
        "📊 Columns",
        summary["Columns"]
    )


with c3:

    st.metric(
        "⚠️ Missing Values",
        summary["Missing"]
    )


with c4:

    st.metric(
        "🔁 Duplicate Rows",
        summary["Duplicates"]
    )


st.markdown("---")


# =========================================================
# BUSINESS HEALTH SCORE
# =========================================================

st.subheader("💚 Business Health Score")


try:

    score = float(score)

except Exception:

    score = 0


score = max(0, min(100, score))


st.progress(
    score / 100
)


if score >= 90:

    st.success(
        f"🟢 Excellent Dataset Quality — {score:.0f}/100"
    )

elif score >= 75:

    st.info(
        f"🔵 Good Dataset Quality — {score:.0f}/100"
    )

elif score >= 60:

    st.warning(
        f"🟡 Average Dataset Quality — {score:.0f}/100"
    )

else:

    st.error(
        f"🔴 Dataset Needs Improvement — {score:.0f}/100"
    )


st.markdown("---")


# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

st.subheader("📄 Executive Summary")


st.info(
    f"""
    **Dataset Size:** {summary['Rows']:,} rows × {summary['Columns']} columns

    **Missing Values:** {summary['Missing']:,}

    **Duplicate Rows:** {summary['Duplicates']:,}

    **Business Health Score:** {score:.0f}/100

    The AI Business Copilot evaluates your dataset and
    provides recommendations, risks, opportunities and
    decision-support insights.
    """
)


st.markdown("---")


# =========================================================
# AI RECOMMENDATIONS
# =========================================================

left, right = st.columns(
    [2, 1],
    gap="large"
)


# =========================================================
# LEFT - RECOMMENDATIONS
# =========================================================

with left:

    st.subheader("🤖 AI Recommendations")

    try:

        recommendations = copilot.recommendations()

        if recommendations:

            for recommendation in recommendations:

                st.success(
                    f"💡 {recommendation}"
                )

        else:

            st.info(
                "No additional recommendations were generated."
            )

    except Exception:

        st.warning(
            "AI recommendations are currently unavailable."
        )


# =========================================================
# RIGHT - NEXT STEPS
# =========================================================

with right:

    st.subheader("⚡ Suggested Next Steps")

    st.info("📊 Analyze Dataset")

    st.info("⚙️ Train AutoML")

    st.info("📈 Generate Forecast")

    st.info("🎯 Predict Business Outcomes")

    st.info("📄 Generate Executive Report")


st.markdown("---")


# =========================================================
# BUSINESS RISK ANALYSIS
# =========================================================

st.subheader("🚨 Business Risk Analysis")


risks = []


if summary["Missing"] > 0:

    risks.append(
        "Missing values may reduce machine learning performance."
    )


if summary["Duplicates"] > 0:

    risks.append(
        "Duplicate records may introduce bias into analysis and models."
    )


if len(df.columns) < 5:

    risks.append(
        "The dataset contains limited features for advanced analysis."
    )


if len(df) < 100:

    risks.append(
        "The dataset contains relatively few records for reliable modeling."
    )


if len(risks) == 0:

    st.success(
        "🟢 No major business risks detected."
    )

else:

    for risk in risks:

        st.warning(
            f"⚠️ {risk}"
        )


st.markdown("---")


# =========================================================
# AI OPPORTUNITIES
# =========================================================

st.subheader("🚀 AI Opportunities")


opportunities = [

    "Forecast future business trends",

    "Predict customer behaviour",

    "Detect unusual or anomalous records",

    "Build executive dashboards",

    "Improve business decision making",

    "Generate automated business reports"

]


for opportunity in opportunities:

    st.success(
        f"🚀 {opportunity}"
    )


st.markdown("---")


# =========================================================
# AI BUSINESS CHAT
# =========================================================

st.subheader("💬 Ask AI Business Copilot")


question = st.text_input(
    "Ask a business question",
    placeholder="Example: What are the major problems in this dataset?"
)


example_questions = [

    "Summarize this dataset",

    "What are the data quality issues?",

    "How ready is this dataset for machine learning?",

    "Give me business recommendations",

    "What risks do you identify?",

    "What AI solutions can be applied to this dataset?"

]


selected_question = st.selectbox(
    "Or choose a sample question",
    [""] + example_questions
)


if selected_question:

    question = selected_question


if question:

    with st.spinner("🤖 Nex Decision AI is analyzing your question..."):

        try:

            answer = copilot.ask(question)

            st.markdown("### 🤖 Nex Decision AI Response")

            if hasattr(answer, "shape"):

                st.dataframe(
                    answer,
                    use_container_width=True
                )

            elif isinstance(answer, list):

                for item in answer:
                    st.success(str(item))

            elif isinstance(answer, tuple):

                st.write(answer)

            else:

                st.info(str(answer))

        except Exception:

            st.warning(
                "Nex Decision AI could not generate a response "
                "for this question using the current dataset. "
                "Please try another business question."
            )

        

st.markdown("---")


# =========================================================
# AI INSIGHT
# =========================================================

ai_insight(
    "The AI Business Copilot helps executives understand "
    "data quality, identify opportunities, assess risks, "
    "and make data-driven decisions before building "
    "machine learning models."
)


# =========================================================
# FOOTER
# =========================================================

page_footer()