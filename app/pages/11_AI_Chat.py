import streamlit as st

from src.ai_chat.chat_engine import ChatEngine
from src.ui.layout import page_header, ai_insight, page_footer

st.set_page_config(
    page_title="AI Chat",
    page_icon="🤖",
    layout="wide"
)

page_header(
    "💬 AI Business Chatbot",
    "Ask questions about your business data using Artificial Intelligence."
)

# --------------------------------------------------
# CHECK DATASET
# --------------------------------------------------

if "dataset" not in st.session_state:

    st.warning("⚠ Please upload a dataset first.")

    st.stop()

df = st.session_state["dataset"]

engine = ChatEngine()

# --------------------------------------------------
# DATASET OVERVIEW
# --------------------------------------------------

st.success("✅ Dataset Loaded Successfully")

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
# CHAT HISTORY
# --------------------------------------------------

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

st.subheader("💬 Ask AI")

question = st.text_input(
    "Ask a question about your dataset"
)

c1, c2 = st.columns([1, 1])

with c1:

    ask = st.button("🤖 Ask AI")

with c2:

    clear = st.button("🗑 Clear Chat")

# --------------------------------------------------
# CLEAR CHAT
# --------------------------------------------------

if clear:

    st.session_state.chat_history = []

    st.rerun()

# --------------------------------------------------
# ASK AI
# --------------------------------------------------

if ask:

    if question.strip() == "":

        st.warning("⚠ Please enter a question.")

    else:

        with st.spinner("🤖 AI is analyzing your dataset..."):

            answer = engine.ask(df, question)

        st.session_state.chat_history.append(

            ("You", question)

        )

        st.session_state.chat_history.append(

            ("AI", answer)

        )

        st.success("✅ Response Generated")

# --------------------------------------------------
# CHAT WINDOW
# --------------------------------------------------

st.subheader("📝 Conversation")

if len(st.session_state.chat_history) == 0:

    st.info("Start the conversation by asking a question.")

else:

    for sender, message in st.session_state.chat_history:

        if sender == "You":

            with st.chat_message("user"):

                st.write(message)

        else:

            with st.chat_message("assistant"):

                st.write(message)

st.divider()

# --------------------------------------------------
# SAMPLE QUESTIONS
# --------------------------------------------------

st.subheader("💡 Example Questions")

st.info("""
• How many rows are in my dataset?

• Which column has the most missing values?

• What are the numeric columns?

• Which features are useful for machine learning?

• Is this dataset suitable for prediction?

• What preprocessing should I perform?
""")

# --------------------------------------------------
# AI INSIGHT
# --------------------------------------------------

ai_insight(
    "The AI Business Chatbot helps users understand datasets through natural language conversations and provides intelligent business insights."
)

page_footer()