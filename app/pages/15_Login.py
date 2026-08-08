import streamlit as st

from src.database.database import Database
from src.auth.auth import Auth
from src.ui.layout import page_header, ai_insight, page_footer

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

page_header(
    "🔐 Secure Login",
    "Access the AI-Driven Decision Intelligence Platform."
)

database = Database()
auth = Auth()

# --------------------------------------------------
# SESSION
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --------------------------------------------------
# ALREADY LOGGED IN
# --------------------------------------------------

if st.session_state.logged_in:

    st.success(
        f"Welcome back, **{st.session_state['username']}** 👋"
    )

    st.info(
        "You are already logged in."
    )

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False

        st.session_state.username = ""

        st.success("Logged out successfully.")

        st.rerun()

    ai_insight(
        "Authentication protects business datasets and machine learning models from unauthorized access."
    )

    page_footer()

    st.stop()

# --------------------------------------------------
# MENU
# --------------------------------------------------

menu = st.radio(

    "Choose an Option",

    [

        "🔑 Login",

        "📝 Register"

    ],

    horizontal=True

)

st.divider()

# ==================================================
# REGISTER
# ==================================================

if menu == "📝 Register":

    st.subheader("📝 Create New Account")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Create Account"):

        if username.strip() == "" or password.strip() == "":

            st.warning(
                "Username and Password cannot be empty."
            )

        elif password != confirm:

            st.error(
                "Passwords do not match."
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
                    "Please login using your new credentials."
                )

            except Exception:

                st.error(
                    "Username already exists."
                )

# ==================================================
# LOGIN
# ==================================================

else:

    st.subheader("🔑 User Login")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username.strip() == "" or password.strip() == "":

            st.warning(
                "Please enter username and password."
            )

        else:

            user = database.get_user(username)

            if user is None:

                st.error(
                    "User not found."
                )

            else:

                if auth.verify_password(
                    password,
                    user[2]
                ):

                    st.session_state.logged_in = True

                    st.session_state.username = username

                    st.success(
                        f"🎉 Welcome, {username}!"
                    )

                    st.balloons()

                    st.info(
                        "You can now access all AI modules."
                    )

                else:

                    st.error(
                        "Incorrect password."
                    )

# --------------------------------------------------
# AI INSIGHT
# --------------------------------------------------

ai_insight(
    "Secure authentication ensures that business data, trained AI models, and executive reports remain accessible only to authorized users."
)

page_footer()