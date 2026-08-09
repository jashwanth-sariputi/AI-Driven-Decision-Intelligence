import streamlit as st
import os
import sys

from src.database.database import Database
from src.auth.auth import Auth

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Nex Decision AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #f5f7fb;
    }

    /* Remove unnecessary top spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Main title */
    .nex-title {
        font-size: 38px;
        font-weight: 800;
        color: #172033;
        margin-bottom: 5px;
    }

    .nex-subtitle {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    /* Login card */
    .login-card {
        background: white;
        padding: 40px;
        border-radius: 18px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        border: 1px solid #e8ebf0;
        min-height: 500px;
    }

    /* About card */
    .about-card {
        background: linear-gradient(
            145deg,
            #172554,
            #1e3a8a
        );
        padding: 45px;
        border-radius: 18px;
        color: white;
        min-height: 500px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }

    .about-card h1 {
        color: white;
        font-size: 36px;
        font-weight: 800;
    }

    .about-card h3 {
        color: #dbeafe;
        margin-top: 25px;
    }

    .about-card p {
        color: #e5e7eb;
        font-size: 16px;
        line-height: 1.7;
    }

    .feature {
        background: rgba(255,255,255,0.10);
        padding: 12px 16px;
        border-radius: 10px;
        margin-top: 10px;
        color: #f8fafc;
    }

    /* Login buttons */
    .stButton > button {
        width: 100%;
        border-radius: 9px;
        height: 45px;
        font-weight: 600;
    }

    /* Hide Streamlit default menu/footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------------------------------------------------
# DATABASE / AUTH
# ---------------------------------------------------------

database = Database()
auth = Auth()

# ---------------------------------------------------------
# ALREADY LOGGED IN
# ---------------------------------------------------------

if st.session_state.logged_in:

    st.success(
        f"Welcome back, {st.session_state.username} 👋"
    )

    st.info(
        "You are already logged in to Nex Decision AI."
    )

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.success("Logged out successfully.")

        st.rerun()

    st.stop()

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="nex-title">Nex Decision AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="nex-subtitle">'
    'AI-powered business intelligence and decision support platform'
    '</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# TWO PANEL LAYOUT
# ---------------------------------------------------------

left, right = st.columns(
    [1, 1.15],
    gap="large"
)

# =========================================================
# LEFT PANEL - LOGIN
# =========================================================

with left:

    st.markdown(
        '<div class="login-card">',
        unsafe_allow_html=True
    )

    st.subheader("🔐 Welcome Back")

    st.write(
        "Sign in to access your AI-powered business analytics."
    )

    st.markdown("---")

    menu = st.radio(
        "Account",
        ["🔑 Login", "📝 Register"],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # -----------------------------------------------------
    # LOGIN
    # -----------------------------------------------------

    if menu == "🔑 Login":

        username = st.text_input(
            "Email / Username",
            placeholder="Enter your email or username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        if st.button(
            "🚀 Login",
            use_container_width=True
        ):

            if (
                username.strip() == ""
                or password.strip() == ""
            ):

                st.warning(
                    "Please enter your username and password."
                )

            else:

                user = database.get_user(username)

                if user is None:

                    st.error(
                        "We couldn't find an account with those details."
                    )

                else:

                    try:

                        valid = auth.verify_password(
                            password,
                            user[2]
                        )

                        if valid:

                            st.session_state.logged_in = True
                            st.session_state.username = username

                            st.success(
                                "Login successful! Welcome to Nex Decision AI."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "The password you entered is incorrect."
                            )

                    except Exception:

                        st.error(
                            "We couldn't complete the login. "
                            "Please try again."
                        )

    # -----------------------------------------------------
    # REGISTER
    # -----------------------------------------------------

    else:

        st.subheader("📝 Create Account")

        username = st.text_input(
            "Email / Username",
            placeholder="Enter your email or username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm your password"
        )

        if st.button(
            "✨ Create Account",
            use_container_width=True
        ):

            if (
                username.strip() == ""
                or password.strip() == ""
            ):

                st.warning(
                    "Please complete all required fields."
                )

            elif password != confirm:

                st.error(
                    "The passwords do not match."
                )

            elif len(password) < 6:

                st.warning(
                    "Password should contain at least 6 characters."
                )

            else:

                try:

                    hashed = auth.hash_password(password)

                    database.create_user(
                        username,
                        hashed
                    )

                    st.success(
                        "🎉 Account created successfully!"
                    )

                    st.info(
                        "You can now switch to Login and sign in."
                    )

                except Exception:

                    st.error(
                        "An account with this username already exists."
                    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# =========================================================
# RIGHT PANEL - ABOUT NEX DECISION AI
# =========================================================

with right:

    st.markdown(
        """
        <div class="about-card">

            <h1>🤖 Nex Decision AI</h1>

            <p>
            Nex Decision AI is an intelligent business analytics
            platform designed to transform raw business data into
            meaningful insights and better decisions.
            </p>

            <h3>What can Nex Decision AI do?</h3>

            <div class="feature">
            📊 Analyze business datasets
            </div>

            <div class="feature">
            🧠 Generate intelligent business insights
            </div>

            <div class="feature">
            🎯 Predict future business outcomes
            </div>

            <div class="feature">
            📈 Forecast business trends
            </div>

            <div class="feature">
            🤖 Automate machine learning workflows
            </div>

            <div class="feature">
            🔍 Explain AI predictions
            </div>

            <div class="feature">
            🚨 Detect business anomalies and risks
            </div>

            <div class="feature">
            💬 Interact with AI through business chat
            </div>

            <h3>Built for smarter decisions</h3>

            <p>
            From dataset intelligence and forecasting to
            prediction, dashboards, explainable AI and
            executive reporting, Nex Decision AI brings
            multiple decision-support capabilities together
            in one platform.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Nex Decision AI • Intelligent Analytics • Smarter Decisions"
)