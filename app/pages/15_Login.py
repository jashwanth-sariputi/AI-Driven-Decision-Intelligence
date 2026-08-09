import streamlit as st

from src.database.database import Database
from src.auth.auth import Auth


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Nex Decision AI",
    page_icon="🔐",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ==============================
       MAIN APPLICATION
       ============================== */

    .stApp {
        background: #080d16;
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2rem;
        max-width: 1250px;
    }


    /* ==============================
       TWO PANELS
       ============================== */

    .login-card {
        background: #101827;
        border: 1px solid #263449;
        border-radius: 18px;
        padding: 38px;
        min-height: 620px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.30);
    }


    /* ==============================
       BRAND
       ============================== */

    .brand {
        font-size: 34px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 35px;
    }

    .brand-accent {
        color: #3b82f6;
    }


    /* ==============================
       LOGIN TEXT
       ============================== */

    .welcome {
        font-size: 30px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 25px;
    }


    /* ==============================
       ABOUT PANEL
       ============================== */

    .about-title {
        font-size: 32px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 15px;
    }

    .about-text {
        color: #cbd5e1;
        font-size: 15px;
        line-height: 1.7;
    }


    /* ==============================
       FEATURE BOXES
       ============================== */

    .feature-box {
        background: #0c1422;
        border: 1px solid #263449;
        border-radius: 12px;
        padding: 14px 16px;
        margin-top: 12px;
    }

    .feature-title {
        color: #ffffff;
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 4px;
    }

    .feature-text {
        color: #94a3b8;
        font-size: 13px;
        line-height: 1.5;
    }


    /* ==============================
       STATUS
       ============================== */

    .status {
        color: #22c55e;
        font-weight: 600;
        margin-top: 25px;
        font-size: 14px;
    }


    /* ==============================
       STREAMLIT INPUTS
       ============================== */

    div[data-baseweb="input"] {
        background-color: #111827 !important;
        border-color: #334155 !important;
    }

    div[data-baseweb="input"] input {
        color: #ffffff !important;
    }


    /* ==============================
       BUTTONS
       ============================== */

    div.stButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 45px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


database = Database()
auth = Auth()


# =========================================================
# ALREADY LOGGED IN
# =========================================================

if st.session_state.logged_in:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:80px 20px 40px 20px;
        ">
            <div style="font-size:55px;">👋</div>

            <div style="
                font-size:34px;
                font-weight:800;
                color:#ffffff;
                margin-top:15px;
            ">
                Welcome back to
                <span style="color:#3b82f6;">
                    Nex Decision AI
                </span>
            </div>

            <div style="
                color:#94a3b8;
                font-size:17px;
                margin-top:10px;
            ">
                Your intelligent business decision platform is ready.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.success(
        f"Signed in as **{st.session_state.username}**"
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.username = ""

            st.rerun()

    st.stop()


# =========================================================
# TWO PANEL LAYOUT
# =========================================================

left, right = st.columns(
    [1, 1],
    gap="large"
)


# =========================================================
# LEFT PANEL — LOGIN / REGISTER
# =========================================================

with left:

    st.markdown(
        """
        <div class="login-card">

            <div class="brand">
                Nex
                <span class="brand-accent">
                    Decision AI
                </span>
            </div>

            <div class="welcome">
                Welcome back
            </div>

            <div class="subtitle">
                Sign in to access your intelligent
                business decision platform.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    menu = st.radio(
        "Account",
        [
            "🔑 Sign In",
            "📝 Create Account"
        ],
        horizontal=True
    )


    # =====================================================
    # LOGIN
    # =====================================================

    if menu == "🔑 Sign In":

        st.subheader("Sign in to your account")

        username = st.text_input(
            "Email Address",
            placeholder="Enter your registered email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        if st.button(
            "🚀 Sign In",
            use_container_width=True
        ):

            if not username.strip() or not password.strip():

                st.warning(
                    "Please enter your email address and password."
                )

            else:

                try:

                    user = database.get_user(
                        username.strip()
                    )

                    if user is None:

                        st.error(
                            "We couldn't find an account with that email."
                        )

                    elif auth.verify_password(
                        password,
                        user[2]
                    ):

                        st.session_state.logged_in = True
                        st.session_state.username = username.strip()

                        st.success(
                            "Welcome to Nex Decision AI! 🎉"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "The password you entered is incorrect. "
                            "Please try again."
                        )

                except Exception:

                    st.error(
                        "We couldn't complete the sign-in. "
                        "Please try again."
                    )


    # =====================================================
    # REGISTER
    # =====================================================

    else:

        st.subheader("Create your account")

        username = st.text_input(
            "Email Address",
            placeholder="Enter your email address"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password"
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True
        ):

            if not username.strip() or not password.strip():

                st.warning(
                    "Please enter your email address and password."
                )

            elif password != confirm:

                st.error(
                    "The passwords do not match."
                )

            elif len(password) < 6:

                st.warning(
                    "Please use a password with at least 6 characters."
                )

            else:

                try:

                    hashed = auth.hash_password(
                        password
                    )

                    database.create_user(
                        username.strip(),
                        hashed
                    )

                    st.success(
                        "🎉 Your account has been created successfully!"
                    )

                    st.info(
                        "You can now sign in using your registered email."
                    )

                except Exception:

                    st.error(
                        "An account with this email already exists."
                    )


# =========================================================
# RIGHT PANEL — ABOUT NEX DECISION AI
# =========================================================

with right:

    st.markdown(
        """
        <div class="login-card">

            st.markdown("""
            <div class="about-title">
                Nex Decision AI
            </div>

            <div class="about-text">
                An AI-powered business intelligence and decision support platform
                designed to transform raw business data into meaningful,
                intelligent, and actionable decisions.
            </div>
            """, unsafe_allow_html=True)

            

            <div class="feature-box">

                <div class="feature-title">
                    🧠 Dataset Intelligence
                </div>

                <div class="feature-text">
                    Automatically understand datasets, identify
                    important columns and evaluate data quality.
                </div>

            </div>


            <div class="feature-box">

                <div class="feature-title">
                    📊 Intelligent Dashboards
                </div>

                <div class="feature-text">
                    Transform business data into interactive
                    dashboards, KPIs and visual insights.
                </div>

            </div>


            <div class="feature-box">

                <div class="feature-title">
                    🤖 AI Business Insights
                </div>

                <div class="feature-text">
                    Generate intelligent recommendations to
                    support better business decisions.
                </div>

            </div>


            <div class="feature-box">

                <div class="feature-title">
                    📈 Forecasting & Prediction
                </div>

                <div class="feature-text">
                    Use machine learning models to forecast
                    trends and generate future predictions.
                </div>

            </div>


            <div class="feature-box">

                <div class="feature-title">
                    🔍 Explainable AI
                </div>

                <div class="feature-text">
                    Understand why machine learning models
                    produce their predictions.
                </div>

            </div>


            <div class="feature-box">

                <div class="feature-title">
                    🚨 AI Anomaly Detection
                </div>

                <div class="feature-text">
                    Detect unusual patterns and identify
                    potential business risks automatically.
                </div>

            </div>


            <div class="status">
                ● AI Engine Ready
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )