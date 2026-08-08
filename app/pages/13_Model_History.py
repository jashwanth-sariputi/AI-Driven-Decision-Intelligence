import streamlit as st
import pandas as pd

from src.database.database import Database
from src.ui.layout import page_header, ai_insight, page_footer

st.set_page_config(
    page_title="Model History",
    page_icon="🏆",
    layout="wide"
)

page_header(
    "🤖 Model History",
    "Review and compare previously trained machine learning models."
)

# --------------------------------------------------
# LOAD DATABASE
# --------------------------------------------------

database = Database()

models = database.get_models()

# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------

if len(models) == 0:

    st.info("🤖 No AI models have been trained yet.")

    ai_insight(
        "Train your first machine learning model using the AutoML Engine."
    )

    page_footer()

    st.stop()

# --------------------------------------------------
# DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(

    models,

    columns=[
        "ID",
        "Dataset",
        "Model",
        "Score",
        "Problem Type",
        "Created At"
    ]

)

# --------------------------------------------------
# SEARCH
# --------------------------------------------------

search = st.text_input(
    "🔍 Search Model"
)

if search:

    df = df[
        df["Model"]
        .astype(str)
        .str.contains(search, case=False)
    ]

# --------------------------------------------------
# LEADERBOARD
# --------------------------------------------------

leaderboard = df.sort_values(
    by="Score",
    ascending=False
)

best_model = leaderboard.iloc[0]

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

st.subheader("📊 Model Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Models Trained",
        len(df)
    )

with c2:

    st.metric(
        "Best Score",
        round(float(df["Score"].max()), 2)
    )

with c3:

    st.metric(
        "Problem Types",
        df["Problem Type"].nunique()
    )

with c4:

    st.metric(
        "Datasets Used",
        df["Dataset"].nunique()
    )

st.divider()

# --------------------------------------------------
# BEST MODEL
# --------------------------------------------------

st.subheader("🥇 Best Performing Model")

st.success(
    f"""
**Model :** {best_model['Model']}

**Dataset :** {best_model['Dataset']}

**Score :** {round(float(best_model['Score']),2)}

**Problem Type :** {best_model['Problem Type']}
"""
)

st.divider()

# --------------------------------------------------
# MODEL HISTORY
# --------------------------------------------------

st.subheader("📋 Model Leaderboard")

st.dataframe(
    leaderboard,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# PERFORMANCE CHART
# --------------------------------------------------

st.subheader("📈 Model Performance")

chart = leaderboard.set_index("Model")["Score"]

st.bar_chart(chart)

st.divider()

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

csv = leaderboard.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Model History",
    csv,
    "model_history.csv",
    "text/csv"
)

# --------------------------------------------------
# AI INSIGHT
# --------------------------------------------------

ai_insight(
    "Model History enables users to compare trained models, evaluate performance, identify the best-performing algorithms, and support informed deployment decisions."
)

page_footer()