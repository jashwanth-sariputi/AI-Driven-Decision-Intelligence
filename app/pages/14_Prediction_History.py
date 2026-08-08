import streamlit as st
import pandas as pd
import plotly.express as px

from src.database.database import Database
from src.ui.layout import page_header, ai_insight, page_footer

st.set_page_config(
    page_title="Prediction History",
    page_icon="📜",
    layout="wide"
)

page_header(
    "📜 Prediction History",
    "Review all previous prediction results."
)

st.caption(
    "View all prediction jobs performed using the AI Prediction Engine."
)

st.markdown("---")

database = Database()

history = database.get_predictions()

# ----------------------------------------------------
# No History
# ----------------------------------------------------

if len(history) == 0:

    st.info("No prediction history available.")

    st.stop()

# ----------------------------------------------------
# DataFrame
# ----------------------------------------------------

history_df = pd.DataFrame(

    history,

    columns=[
        "ID",
        "Model",
        "Filename",
        "Rows",
        "Prediction Time"
    ]

)

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

st.subheader("📈 Prediction Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Predictions",
        len(history_df)
    )

with c2:
    st.metric(
        "Models Used",
        history_df["Model"].nunique()
    )

with c3:
    st.metric(
        "Datasets Predicted",
        history_df["Filename"].nunique()
    )

st.markdown("---")

# ----------------------------------------------------
# Prediction Table
# ----------------------------------------------------

st.subheader("📋 Prediction Records")

st.dataframe(
    history_df,
    use_container_width=True
)

# ----------------------------------------------------
# Charts
# ----------------------------------------------------

st.markdown("---")

st.subheader("📊 Prediction Analytics")

model_count = (
    history_df["Model"]
    .value_counts()
    .reset_index()
)

model_count.columns = ["Model", "Predictions"]

fig = px.bar(
    model_count,
    x="Model",
    y="Predictions",
    text="Predictions",
    title="Predictions by Model"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

fig = px.pie(
    model_count,
    names="Model",
    values="Predictions",
    title="Model Usage Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Download
# ----------------------------------------------------

st.markdown("---")

csv = history_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Prediction History",
    data=csv,
    file_name="prediction_history.csv",
    mime="text/csv"
)

st.success("Prediction history loaded successfully.")
ai_insight(
    "Prediction history stores all prediction activities for auditing and business tracking."
)

page_footer()