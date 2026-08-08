import streamlit as st
import pandas as pd

from src.database.database import Database
from src.ui.layout import page_header, ai_insight, page_footer

st.set_page_config(
    page_title="Dataset History",
    page_icon="📂",
    layout="wide"
)

page_header(
    "📂 Dataset History",
    "View and manage all datasets uploaded to the platform."
)

# --------------------------------------------------
# LOAD DATABASE
# --------------------------------------------------

database = Database()

history = database.get_uploads()

# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------

if len(history) == 0:

    st.info("📂 No datasets have been uploaded yet.")

    ai_insight(
        "Upload a dataset to begin AI-powered business analytics."
    )

    page_footer()

    st.stop()

# --------------------------------------------------
# DATAFRAME
# --------------------------------------------------

history_df = pd.DataFrame(

    history,

    columns=[
        "ID",
        "Filename",
        "Rows",
        "Columns",
        "Dataset Type",
        "Upload Time"
    ]

)

# --------------------------------------------------
# SEARCH
# --------------------------------------------------

search = st.text_input(
    "🔍 Search Dataset"
)

if search:

    history_df = history_df[
        history_df["Filename"]
        .astype(str)
        .str.contains(search, case=False)
    ]

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

st.subheader("📊 Upload Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Datasets",
        len(history_df)
    )

with c2:

    st.metric(
        "Total Rows",
        int(history_df["Rows"].sum())
    )

with c3:

    st.metric(
        "Total Columns",
        int(history_df["Columns"].sum())
    )

with c4:

    st.metric(
        "Dataset Types",
        history_df["Dataset Type"].nunique()
    )

st.divider()

# --------------------------------------------------
# HISTORY TABLE
# --------------------------------------------------

st.subheader("📋 Upload History")

st.dataframe(
    history_df,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# DATASET TYPE DISTRIBUTION
# --------------------------------------------------

st.subheader("📈 Dataset Type Distribution")

dataset_count = (
    history_df["Dataset Type"]
    .value_counts()
    .reset_index()
)

dataset_count.columns = [
    "Dataset Type",
    "Count"
]

st.bar_chart(
    dataset_count.set_index("Dataset Type")
)

st.divider()

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

csv = history_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Dataset History",
    csv,
    "dataset_history.csv",
    "text/csv"
)

# --------------------------------------------------
# AI INSIGHT
# --------------------------------------------------

ai_insight(
    "Dataset History provides a centralized record of uploaded datasets, helping users monitor data usage, manage projects, and maintain traceability."
)

page_footer()