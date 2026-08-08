import streamlit as st
from src.ui.layout import page_header, ai_insight, page_footer
from src.ui.cards import kpi_card

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.dashboard_ai.visualization_recommender import VisualizationRecommender
from src.database.database import Database

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

page_header(
    "📊 Executive Dashboard",
    "Executive Business KPIs, AI Insights & Decision Intelligence"
)

st.markdown("""
### 🚀 Executive Decision Center

This dashboard automatically summarizes your business dataset,
highlights key performance indicators, evaluates data quality,
and provides AI-driven recommendations for executive decision-making.
""")

st.divider()

# ==========================================================
# DATASET CHECK
# ==========================================================

if "dataset" not in st.session_state:

    st.warning("Please upload a dataset first.")

    st.stop()

df = st.session_state["dataset"]


database = Database()
models = database.get_models()
predictions = database.get_predictions()

ai_dashboard = VisualizationRecommender(df)

recommendations = ai_dashboard.recommend()
st.success("✅ Step 2 : AI Recommendations Generated")
st.success("✅ Dataset Loaded Successfully")

# ==========================================================
# DATASET OVERVIEW
# ==========================================================

rows = len(df)

columns = len(df.columns)

missing = int(df.isnull().sum().sum())

duplicates = int(df.duplicated().sum())

numeric_cols = df.select_dtypes(include="number").columns

cat_cols = df.select_dtypes(exclude="number").columns

score = 100

score -= min(missing * 2, 30)

score -= min(duplicates * 2, 20)

score = max(score, 0)

if score >= 90:

    grade = "🟢 Excellent"

elif score >= 75:

    grade = "🟡 Good"

elif score >= 60:

    grade = "🟠 Average"

else:

    grade = "🔴 Poor"

# ==========================================================
# KPI SUMMARY
# ==========================================================

st.subheader("📌 Executive KPI Summary")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    kpi_card("Rows", rows)

with c2:
    kpi_card("Columns", columns)

with c3:
    kpi_card("Missing", missing)

with c4:
    kpi_card("Duplicates", duplicates)

with c5:
    kpi_card("Health", f"{score}/100")

st.divider()

# ==========================================================
# BUSINESS HEALTH
# ==========================================================
st.divider()

st.header("🏢 Business Overview")

st.info(f"""
### Executive Business Summary

• **Dataset Name:** {st.session_state.get("filename", "Unknown")}

• **Total Business Records:** {len(df):,}

• **Available Features:** {len(df.columns)}

• **Business Health Score:** {score}/100

• **Missing Values:** {missing}

• **Duplicate Records:** {duplicates}

This dashboard provides a comprehensive overview of your business data and is ready for AI-powered analytics, machine learning, forecasting, and executive reporting.
""")
st.subheader("🏥 Business Health Score")


left, right = st.columns([2,1])

with left:

    st.progress(score / 100)

    st.metric(
        "Overall Health",
        f"{score}/100"
    )

with right:

    st.metric(
        "Grade",
        grade
    )

st.divider()

# ==========================================================
# LATEST MODEL
# ==========================================================
st.success("Before Database")

try:


    st.success("Database Connected")

    models


    st.success("Models Loaded")

except Exception as e:

    st.error(e)

    st.stop()
st.success("✅ Step 3 : Model History Loaded")

if len(models) > 0:

    latest = models[0]

    st.subheader("🤖 Latest Trained AI Model")

    c1, c2, c3 = st.columns(3)

    with c1:
        kpi_card("Model", latest[2])

    with c2:
        kpi_card("Performance", f"{latest[3]:.2f}")

    with c3:
        kpi_card("Problem Type", latest[4])

st.divider()

# ==========================================================
# LATEST PREDICTION
# ==========================================================

predictions

if len(predictions) > 0:

    latest = predictions[0]

    st.subheader("🔮 Latest Prediction")

    c1, c2, c3 = st.columns(3)

    with c1:
        kpi_card("Model", latest[1])

    with c2:
        kpi_card("Rows Predicted", latest[3])

    with c3:
        kpi_card("Dataset", latest[2])

st.divider()

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.subheader("📈 Executive Summary")
st.divider()

st.header("📌 Executive KPI Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Dataset Rows",
        len(df)
    )

with c2:
    st.metric(
        "Dataset Columns",
        len(df.columns)
    )

with c3:
    st.metric(
        "Numeric Features",
        len(numeric_cols)
    )

with c4:
    st.metric(
        "Categorical Features",
        len(cat_cols)
    )

summary = f"""
**Dataset Statistics**

• Total Records : **{rows:,}**

• Total Columns : **{columns}**

• Numeric Features : **{len(numeric_cols)}**

• Categorical Features : **{len(cat_cols)}**

• Missing Values : **{missing}**

• Duplicate Records : **{duplicates}**

Overall, this dataset is suitable for business intelligence,
machine learning and predictive analytics.
"""

st.info(summary)

st.divider()

# ==========================================================
# DATA QUALITY ALERTS
# ==========================================================
st.divider()

st.header("🤖 AI Executive Insights")

insights = []

if score >= 90:
    insights.append("✅ Dataset quality is excellent and suitable for AI model deployment.")

elif score >= 75:
    insights.append("🟡 Dataset quality is good. Minor preprocessing is recommended.")

else:
    insights.append("🔴 Dataset quality requires cleaning before reliable AI modeling.")

if missing > 0:
    insights.append(f"⚠ Dataset contains {missing} missing values.")

if duplicates > 0:
    insights.append(f"⚠ Dataset contains {duplicates} duplicate records.")

if len(numeric_cols) > 5:
    insights.append("📈 Rich numerical data is available for predictive analytics.")

if len(cat_cols) > 0:
    insights.append("📊 Categorical variables are available for segmentation and business intelligence.")

if len(insights) == 0:
    st.success("No significant issues detected.")

else:
    for insight in insights:
        st.info(insight)
st.subheader("🚨 Data Quality Alerts")

alerts = []

if missing > 0:
    alerts.append(f"⚠ {missing} missing values detected.")

if duplicates > 0:
    alerts.append(f"⚠ {duplicates} duplicate rows detected.")

if len(numeric_cols) < 2:
    alerts.append("⚠ Very few numeric columns available.")

if len(cat_cols) == 0:
    alerts.append("⚠ No categorical columns detected.")

if len(alerts) == 0:

    st.success("✅ Excellent! No major data quality issues detected.")

else:

    for alert in alerts:

        st.warning(alert)

st.divider()

# ==========================================================
# HISTOGRAM
# ==========================================================

if len(numeric_cols) > 0:

    st.subheader("📊 Numeric Distribution")

    column = st.selectbox(
        "Select Numeric Column",
        numeric_cols,
        key="histogram_col"
    )

    fig = px.histogram(
        df,
        x=column,
        nbins=30,
        title=f"Distribution of {column}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="histogram"
    )

# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

if len(numeric_cols) >= 2:

    st.subheader("🔥 Correlation Heatmap")

    corr = df[numeric_cols].corr(numeric_only=True)

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu",
        title="Correlation Matrix"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="heatmap"
    )

# ==========================================================
# PIE CHART
# ==========================================================

if len(cat_cols) > 0:

    st.subheader("🥧 Category Distribution")

    cat = st.selectbox(
        "Category",
        cat_cols,
        key="pie_category"
    )

    counts = (
        df[cat]
        .value_counts()
        .head(10)
        .reset_index()
    )

    counts.columns = [cat, "Count"]

    fig = px.pie(
        counts,
        names=cat,
        values="Count",
        hole=0.45,
        title=f"{cat} Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="pie"
    )

# ==========================================================
# BAR CHART
# ==========================================================

if len(cat_cols) > 0 and len(numeric_cols) > 0:

    st.subheader("📊 Category vs Numeric")

    cat = st.selectbox(
        "Category",
        cat_cols,
        key="bar_category"
    )

    num = st.selectbox(
        "Numeric",
        numeric_cols,
        key="bar_numeric"
    )

    chart = (
        df.groupby(cat)[num]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        chart,
        x=cat,
        y=num,
        color=num,
        title=f"Average {num} by {cat}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="bar"
    )

# ==========================================================
# OUTLIER ANALYSIS
# ==========================================================

if len(cat_cols) > 0 and len(numeric_cols) > 0:

    st.subheader("📦 Outlier Analysis")

    cat = st.selectbox(
        "Category",
        cat_cols,
        key="box_category"
    )

    num = st.selectbox(
        "Numeric",
        numeric_cols,
        key="box_numeric"
    )

    sample_df = df[[cat, num]].dropna()

    if len(sample_df) > 5000:
        sample_df = sample_df.sample(
            5000,
            random_state=42
        )

    fig = px.box(
        sample_df,
        x=cat,
        y=num,
        color=cat,
        title=f"Outlier Analysis - {num}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="boxplot"
    )

# ==========================================================
# LINE CHART
# ==========================================================

if len(numeric_cols) >= 2:

    st.subheader("📈 Trend Analysis")

    x = st.selectbox(
        "X Axis",
        numeric_cols,
        key="line_x"
    )

    y = st.selectbox(
        "Y Axis",
        numeric_cols,
        key="line_y"
    )

    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        title=f"{y} vs {x}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="line"
    )

# ==========================================================
# GEOGRAPHIC ANALYSIS
# ==========================================================

location_columns = []

for col in df.columns:

    name = col.lower()

    if (
        "city" in name
        or "state" in name
        or "country" in name
        or "region" in name
    ):
        location_columns.append(col)

if len(location_columns) > 0:

    st.subheader("🌍 Geographic Analysis")

    location = st.selectbox(
        "Location",
        location_columns,
        key="geo_location"
    )

    geo = (
        df[location]
        .value_counts()
        .head(15)
        .reset_index()
    )

    geo.columns = [location, "Count"]

    fig = px.bar(
        geo,
        x=location,
        y="Count",
        color="Count",
        title="Top Business Locations"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="geo"
    )

# ==========================================================
# DATA PREVIEW
# ==========================================================

st.subheader("📋 Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

st.divider()

# ==========================================================
# EXECUTIVE RECOMMENDATION
# ==========================================================

st.header("💼 Executive Action Center")

col1, col2 = st.columns(2)

with col1:

    st.subheader("📌 Recommended Actions")

    if score >= 90:

        st.success("✅ Deploy AI models")

        st.success("📈 Monitor KPIs")

        st.success("📄 Generate Reports")

        st.success("🚀 Forecast Business Trends")

    elif score >= 75:

        st.info("🔍 Review Missing Values")

        st.info("🤖 Retrain AutoML")

        st.info("📊 Continue Monitoring")

    else:

        st.error("⚠ Clean Dataset")

        st.error("⚠ Remove Duplicates")

        st.error("⚠ Improve Data Quality")

with col2:

    st.subheader("📊 Executive Summary")

    st.metric(
        "Business Health",
        f"{score}/100"
    )

    st.metric(
        "AI Models Trained",
        len(models)
    )

    st.metric(
        "Predictions Generated",
        len(predictions)
    )

    st.metric(
        "Dataset Records",
        len(df)
    )

# ==========================================================
# AI INSIGHT
# ==========================================================

ai_insight(
    "Executives should monitor business health, KPIs, AI model performance, anomalies, and forecasts to support data-driven decision making."
)

page_footer()