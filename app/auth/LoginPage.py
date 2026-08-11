import streamlit as st
import sys
import os

# =========================================================
# PROJECT PATH
# =========================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# =========================================================
# IMPORTS
# =========================================================

from src.database.database import Database
from src.auth.auth import Auth


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Nex Decision AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       MAIN BACKGROUND
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at top left,
                #13284A 0%,
                #07111F 45%,
                #030914 100%
            );
        color: #F8FAFC;
    }

    /* =====================================================
       MAIN CONTENT WIDTH
       ===================================================== */

    .block-container {
        max-width: 1120px;
        padding-top: 35px;
        padding-bottom: 50px;
    }

    /* =====================================================
       HEADER
       ===================================================== */

    .brand-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        color: #F8FAFC;
        margin-bottom: 5px;
    }

    .brand-subtitle {
        font-size: 18px;
        text-align: center;
        color: #93C5FD;
        margin-bottom: 35px;
    }

    /* =====================================================
       PANEL
       ===================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(
            145deg,
            #102A4C,
            #0B1E38
        );

        border: 1px solid #285A91;
        border-radius: 22px;
        padding: 28px;
        box-shadow:
            0 15px 45px rgba(0, 0, 0, 0.35);
    }

    /* =====================================================
       TEXT
       ===================================================== */

    h1, h2, h3 {
        color: #F8FAFC !important;
    }

    .welcome-text {
        color: #BFDBFE;
        font-size: 16px;
        line-height: 1.7;
    }

    .info-text {
        color: #CBD5E1;
        font-size: 15px;
        line-height: 1.7;
    }

    .feature-text {
        color: #CBD5E1;
        font-size: 15px;
        line-height: 1.8;
    }

    /* =====================================================
       INPUTS
       ===================================================== */

    div[data-baseweb="input"] {
        background-color: #172033 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="input"]:focus-within {
        border: 1px solid #3B82F6 !important;
        box-shadow:
            0 0 0 2px rgba(59, 130, 246, 0.15);
    }

    div[data-baseweb="input"] input {
        color: #F8FAFC !important;
        background-color: transparent !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #94A3B8 !important;
    }

    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #3B82F6;
        background: linear-gradient(
            135deg,
            #2563EB,
            #1D4ED8
        );
        color: white;
        font-weight: 700;
        min-height: 44px;
    }

    .stButton > button:hover {
        background: linear-gradient(
            135deg,
            #3B82F6,
            #2563EB
        );
        border-color: #60A5FA;
    }

    /* =====================================================
       RADIO
       ===================================================== */

    div[role="radiogroup"] {
        background: #102A4C;
        border: 1px solid #315D8F;
        border-radius: 12px;
        padding: 8px 12px;
    }

    /* =====================================================
       ALERTS
       ===================================================== */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* =====================================================
       HIDE SIDEBAR
       ===================================================== */

    [data-testid="stSidebar"] {
        display: none;
    }

    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {
        border-color: #28496F;
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


# =========================================================
# DATABASE / AUTH
# =========================================================

database = Database()
auth = Auth()


# =========================================================
# IF ALREADY LOGGED IN
# =========================================================

if st.session_state.logged_in:

    st.markdown(
        "<h1>Welcome back 👋</h1>",
        unsafe_allow_html=True
    )

    st.info(
        f"You are signed in as **{st.session_state.username}**."
    )

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="brand-title">Nex Decision AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="brand-subtitle">'
    'AI-powered business intelligence and decision support platform'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# MAIN PANEL
# =========================================================

with st.container(border=True):

    # -----------------------------------------------------
    # WELCOME
    # -----------------------------------------------------

    st.markdown(
        "## Welcome to Nex Decision AI 👋"
    )

    st.markdown(
        """
        <div class="welcome-text">
        Sign in to your account or create a new account
        to access intelligent business analytics,
        predictions and decision-support tools.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # -----------------------------------------------------
    # ACCOUNT SELECTION
    # -----------------------------------------------------

    menu = st.radio(
        "Account",
        [
            "🔑 Sign In",
            "📝 Create Account"
        ],
        horizontal=True
    )

    st.divider()


    # =====================================================
    # SIGN IN
    # =====================================================

    if menu == "🔑 Sign In":

        st.subheader("Sign in to your account")

        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "🔑 Sign In",
            key="signin_button",
            type="primary"
        ):

            if not username.strip() or not password.strip():

                st.warning(
                    "Please enter your username and password."
                )

            else:

                try:

                    user = database.get_user(
                        username.strip()
                    )

                    if user is None:

                        st.error(
                            "We couldn't find an account "
                            "with that username."
                        )

                    else:

                        password_valid = auth.verify_password(
                            password,
                            user[2]
                        )

                        if password_valid:

                            from datetime import datetime

                            st.session_state.logged_in = True
                            st.session_state.username = username.strip()
                            st.session_state.login_time = datetime.now()

                            st.success(
                                "Login successful! Welcome to Nex Decision AI 🎉"
                            )

                            st.rerun()

                        else:

                            st.error(
                                "The password you entered is incorrect."
                            )

                except Exception as e:

                    st.error(
                        "Unable to complete sign in."
                    )

                    st.caption(
                        f"Error: {str(e)}"
                    )


    # =====================================================
    # CREATE ACCOUNT
    # =====================================================

    else:

        st.subheader("Create your account")

        username = st.text_input(
            "Username",
            placeholder="Choose a username",
            key="register_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="register_confirm"
        )

        if st.button(
            "📝 Create Account",
            key="register_button",
            type="primary"
        ):

            username_clean = username.strip()

            if not username_clean or not password:

                st.warning(
                    "Please enter a username and password."
                )

            elif password != confirm_password:

                st.error(
                    "The passwords do not match."
                )

            elif len(password) < 6:

                st.warning(
                    "Password must contain at least 6 characters."
                )

            else:

                try:

                    # Check whether username already exists
                    existing_user = database.get_user(
                        username_clean
                    )

                    if existing_user is not None:

                        st.error(
                            "That username is already registered."
                        )

                    else:

                        hashed_password = auth.hash_password(
                            password
                        )

                        database.create_user(
                            username_clean,
                            hashed_password
                        )

                        st.success(
                            "Account created successfully! 🎉"
                        )

                        st.info(
                            "Switch to 'Sign In' above "
                            "to access Nex Decision AI."
                        )

                except Exception as e:

                    st.error(
                        "Unable to create the account."
                    )

                    st.caption(
                        f"Error: {str(e)}"
                    )


    # =====================================================
    # PROJECT INFORMATION
    # =====================================================

    st.divider()

    st.markdown(
        "### 🤖 About Nex Decision AI"
    )

    st.markdown(
        """
        <div class="info-text">
        Nex Decision AI is an AI-powered business intelligence
        and decision-support platform that transforms business
        datasets into meaningful insights, predictions,
        forecasts and actionable recommendations.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### What you can do")

    st.markdown(
        """
        <div class="feature-text">

        📊 <b>Analyze business datasets</b><br>

        🧠 <b>Generate intelligent business insights</b><br>

        🎯 <b>Generate AI-powered predictions</b><br>

        📈 <b>Forecast future business trends</b><br>

        🔍 <b>Understand machine learning predictions</b><br>

        📄 <b>Generate executive business reports</b>

        </div>
        """,
        unsafe_allow_html=True
    )