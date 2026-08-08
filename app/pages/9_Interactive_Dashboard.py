import streamlit as st

import pandas as pd

from src.dashboard_visuals.interactive_dashboard import InteractiveDashboard
from src.ui.layout import page_header, ai_insight, page_footer

st.set_page_config(
    page_title="Interactive Dashboard",
    page_icon="📈",
    layout="wide"
)
page_header(
    "📊 Interactive Dashboard",
    "Explore business data through interactive visualizations."
)

if "dataset" not in st.session_state:

    st.warning("Upload a dataset first.")

    st.stop()

df = st.session_state["dataset"]
# Limit rows for interactive visualization
if len(df) > 5000:
    df = df.sample(5000, random_state=42)
    st.info("Showing a random sample of 5,000 rows for faster visualization.")

dashboard = InteractiveDashboard()

numeric = df.select_dtypes(include="number").columns

categorical = df.select_dtypes(include="object").columns

# --------------------

if len(numeric) >= 2:

    st.subheader("Scatter Plot")

    fig = dashboard.scatter(
        df,
        numeric[0],
        numeric[1]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------

# --------------------

if len(categorical) >= 1:

    st.subheader("Pie Chart")

    counts = (
        df[categorical[0]]
        .value_counts()
        .head(10)
        .reset_index()
    )

    counts.columns = ["Category", "Count"]

    fig = dashboard.pie_chart(
        counts,
        "Category",
        "Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
# --------------------

if len(numeric) >= 1:

    st.subheader("Histogram")

    fig = dashboard.histogram(
        df,
        numeric[0]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------

if len(numeric) >= 2:

    st.subheader("Correlation Heatmap")

    corr = df[numeric].corr()

    fig = dashboard.heatmap(corr)

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    ai_insight(
    "Interactive dashboards help decision-makers quickly identify trends, patterns, and business opportunities."
    )

page_footer()