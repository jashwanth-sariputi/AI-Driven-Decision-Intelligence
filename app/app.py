import os
import sys
import streamlit as st


# =========================================================
# PROJECT PATH
# =========================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Nex Decision AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# =========================================================
# LOGIN PAGE
#
# IMPORTANT:
# LoginPage.py is inside app/auth, NOT app/pages.
# Therefore Streamlit will not automatically discover it
# as another page.
# =========================================================

login_page = st.Page(
    "auth/LoginPage.py",
    title="Sign In",
    icon="🔐",
    url_path="signin"
)


# =========================================================
# APPLICATION PAGES
# =========================================================

home_page = st.Page(
    "pages/0_Home.py",
    title="Home",
    icon="🏠"
)

upload_page = st.Page(
    "pages/1_Upload_Dataset.py",
    title="Upload Dataset",
    icon="📂"
)

dataset_page = st.Page(
    "pages/2_Dataset_Intelligence.py",
    title="Dataset Intelligence",
    icon="🧠"
)

copilot_page = st.Page(
    "pages/3_AI_Business_Copilot.py",
    title="AI Business Copilot",
    icon="🤖"
)

executive_page = st.Page(
    "pages/4_Executive_Dashboard.py",
    title="Executive Dashboard",
    icon="📊"
)

automl_page = st.Page(
    "pages/5_AutoML.py",
    title="AutoML",
    icon="⚙️"
)

forecasting_page = st.Page(
    "pages/6_Business_Forecasting.py",
    title="Business Forecasting",
    icon="📈"
)

prediction_page = st.Page(
    "pages/7_Prediction.py",
    title="Prediction",
    icon="🔮"
)

explainable_page = st.Page(
    "pages/8_Explainable_AI.py",
    title="Explainable AI",
    icon="🔍"
)

predictor_page = st.Page(
    "pages/9_AI_Predictor.py",
    title="AI Predictor",
    icon="🎯"
)

interactive_page = st.Page(
    "pages/9_Interactive_Dashboard.py",
    title="Interactive Dashboard",
    icon="📊"
)

kpi_page = st.Page(
    "pages/10_KPI_Dashboard.py",
    title="KPI Dashboard",
    icon="📌"
)

chat_page = st.Page(
    "pages/11_AI_Chat.py",
    title="AI Chat",
    icon="💬"
)

dataset_history_page = st.Page(
    "pages/12_Dataset_History.py",
    title="Dataset History",
    icon="📚"
)

model_history_page = st.Page(
    "pages/13_Model_History.py",
    title="Model History",
    icon="🧪"
)

prediction_history_page = st.Page(
    "pages/14_Prediction_History.py",
    title="Prediction History",
    icon="📜"
)

anomaly_page = st.Page(
    "pages/17_AI_Anomaly_Detection.py",
    title="AI Anomaly Detection",
    icon="🚨"
)

report_page = st.Page(
    "pages/18_Executive_Report.py",
    title="Executive Report",
    icon="📄"
)


# =========================================================
# LOGOUT FUNCTION
# =========================================================

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""


# =========================================================
# BEFORE LOGIN
# =========================================================

if not st.session_state.logged_in:

    pg = st.navigation(
        [login_page],
        position="hidden"
    )

    pg.run()

    st.stop()


# =========================================================
# AFTER LOGIN
# =========================================================

pages = {
    "Nex Decision AI": [
        home_page,
        upload_page,
        dataset_page,
        copilot_page,
        executive_page,
        automl_page,
        forecasting_page,
        prediction_page,
        explainable_page,
        predictor_page,
        interactive_page,
        kpi_page,
        chat_page,
        dataset_history_page,
        model_history_page,
        prediction_history_page,
        anomaly_page,
        report_page
    ]
}


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "## 🤖 Nex Decision AI"
    )

    st.caption(
        f"Signed in as: {st.session_state.username}"
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        logout()
        st.rerun()


# =========================================================
# NAVIGATION
# =========================================================

pg = st.navigation(
    pages,
    position="sidebar"
)

pg.run()