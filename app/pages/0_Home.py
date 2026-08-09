import streamlit as st
from src.ui.theme import sidebar

st.set_page_config(
    page_title=" Nex Decision AI",
    page_icon="🤖",
    layout="wide"
)

sidebar()

# =====================================================
# HERO SECTION
# =====================================================

st.title("🤖  Nex Decision AI")

st.caption("Enterprise Business Analytics Suite powered by Artificial Intelligence")

st.markdown("---")

st.markdown("""
### Welcome 👋

Transform raw business data into intelligent decisions using Machine Learning,
Business Intelligence, Explainable AI, Forecasting, and Executive Analytics.

This platform enables organizations to analyze datasets, build AI models,
predict outcomes, detect anomalies, and automatically generate executive reports.
""")

st.markdown("---")

# =====================================================
# PLATFORM OVERVIEW
# =====================================================


from src.database.database import Database

database = Database()

uploads = database.get_uploads()
models = database.get_models()
predictions = database.get_predictions()

st.subheader("🚀 Platform Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("📂 Datasets", len(uploads))

with c2:
    st.metric("🤖 Models", len(models))

with c3:
    st.metric("🔮 Predictions", len(predictions))

with c4:
    st.metric("✅ Version", "2.2")

st.markdown("---")

# =====================================================
# FEATURES
# =====================================================

st.subheader("✨ Key Features")

left, right = st.columns(2)

with left:

    st.success("📂 Dataset Upload")

    st.success("🔍 Dataset Intelligence")

    st.success("🤖 AI Business Copilot")

    st.success("⚙️ AutoML Engine")

    st.success("🎯 Prediction Engine")

    st.success("🧠 Explainable AI")

with right:

    st.success("📈 Business Forecasting")

    st.success("📊 Executive Dashboard")

    st.success("🚨 AI Anomaly Detection")

    st.success("📄 Executive Report")

    st.success("💬 AI Chat")

    st.success("📚 Dataset & Model History")

st.markdown("---")

# =====================================================
# SUPPORTED DOMAINS
# =====================================================

st.subheader("🏢 Supported Business Domains")

domains = [
    "🛒 E-Commerce",
    "🏥 Healthcare",
    "🏦 Banking",
    "💰 Finance",
    "🏭 Manufacturing",
    "🚚 Supply Chain",
    "📡 Telecom",
    "🎓 Education",
    "👨‍💼 Human Resources",
    "📈 Sales & Marketing"
]

cols = st.columns(2)

for i, domain in enumerate(domains):
    cols[i % 2].info(domain)

st.markdown("---")

# =====================================================
# GETTING STARTED
# =====================================================

st.subheader("📌 Getting Started")

st.markdown("""
1. 📂 Upload your dataset

2. 🔍 Analyze dataset quality

3. 🤖 Explore AI Business Copilot

4. ⚙️ Train AutoML models

5. 🎯 Generate predictions

6. 🧠 Explain model decisions

7. 📈 Forecast future trends

8. 📄 Export Executive Report
""")

st.markdown("---")

# =====================================================
# AI INSIGHT
# =====================================================

st.subheader("🤖 AI Insight")

st.info(
    "Upload a business dataset to unlock AI-powered analytics, "
    "machine learning, forecasting, explainable AI, and executive reporting."
)

st.markdown("---")

# =====================================================
# FOOTER
# =====================================================

st.caption(
    "© 2026 S Jashwanth  | Nex Decision AI | Version 2.0"
)