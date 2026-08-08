import streamlit as st
from src.ui.layout import page_header, ai_insight, page_footer

import pandas as pd
import shap
import matplotlib.pyplot as plt
import joblib
import os

st.set_page_config(
    page_title="Explainable AI",
    page_icon="🧠",
    layout="wide"
)

page_header(
    "🧠 Explainable AI",
    "Understand how your machine learning model makes predictions using SHAP."
)

# =====================================================
# CHECK DATASET
# =====================================================

if "dataset" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state["dataset"]

# =====================================================
# LOAD MODELS
# =====================================================

MODEL_FOLDER = "saved_models"

if not os.path.exists(MODEL_FOLDER):
    st.warning("No trained models found.")
    st.stop()

models = sorted(
    [m for m in os.listdir(MODEL_FOLDER) if m.endswith(".pkl")]
)

if len(models) == 0:
    st.warning("No trained models available.")
    st.stop()

selected_model = st.selectbox(
    "Select Model",
    models
)

# =====================================================
# LOAD MODEL
# =====================================================

package = joblib.load(
    os.path.join(
        MODEL_FOLDER,
        selected_model
    )
)

if isinstance(package, dict):

    model = package["model"]

    feature_names = package.get(
        "feature_names",
        None
    )

    target_column = package.get(
        "target_column",
        None
    )

    problem_type = package.get(
        "problem_type",
        None
    )

else:

    model = package
    feature_names = None
    target_column = None
    problem_type = None

# =====================================================
# MODEL INFORMATION
# =====================================================

st.subheader("📋 Model Information")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Problem Type",
        problem_type if problem_type else "Unknown"
    )

with c2:
    st.metric(
        "Target Column",
        target_column if target_column else "Unknown"
    )

with c3:
    st.metric(
        "Features",
        len(feature_names) if feature_names else len(df.columns)
    )

st.markdown("---")

# =====================================================
# EXPLAINABILITY DASHBOARD
# =====================================================

st.subheader("📈 Explainability Dashboard")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Dataset Rows",
        len(df)
    )

with c2:
    st.metric(
        "Numeric Features",
        len(df.select_dtypes(include="number").columns)
    )

with c3:
    st.metric(
        "Categorical Features",
        len(df.select_dtypes(exclude="number").columns)
    )

st.markdown("---")

# =====================================================
# GENERATE SHAP
# =====================================================

if st.button(
    "🚀 Generate Explainable AI Report",
    use_container_width=True
):

    if feature_names:

        missing_columns = [

            col

            for col in feature_names

            if col not in df.columns

        ]

        if len(missing_columns) > 0:

            st.error("❌ Dataset is not compatible with this model.")

            st.subheader("Missing Columns")

            st.dataframe(
                pd.DataFrame(
                    {
                        "Required Columns": missing_columns
                    }
                ),
                use_container_width=True
            )

            st.info(
                "Please upload the same dataset used for training this model."
            )

            st.stop()

        X = df[feature_names].copy()

    else:

        X = df.copy()

    # Encode categorical columns

    for col in X.columns:

        if X[col].dtype == "object":

            X[col] = (
                X[col]
                .astype("category")
                .cat
                .codes
            )

    X = X.fillna(0)

    if len(X) > 1000:

        X = X.sample(
            1000,
            random_state=42
        )

    with st.spinner("Generating SHAP explanations..."):

        progress = st.progress(10)

        explainer = shap.Explainer(model)

        progress.progress(40)

        shap_values = explainer(
            X,
            check_additivity=False
        )

        progress.progress(100)

    st.success("✅ SHAP Explanation Generated Successfully")

    st.markdown("---")

    # =====================================================
    # FEATURE IMPORTANCE
    # =====================================================

    st.subheader("📊 Global Feature Importance")

    fig = plt.figure(figsize=(10,6))

    shap.plots.bar(
        shap_values,
        show=False
    )

    st.pyplot(fig)

    plt.close()

    st.markdown("---")

    # =====================================================
    # SUMMARY PLOT
    # =====================================================

    st.subheader("🌍 SHAP Summary Plot")

    fig = plt.figure(figsize=(10,6))

    shap.summary_plot(
        shap_values,
        X,
        show=False
    )

    st.pyplot(fig)

    plt.close()

    st.markdown("---")

    # =====================================================
    # FEATURE IMPORTANCE TABLE
    # =====================================================

    importance = pd.DataFrame({

        "Feature": X.columns,

        "Importance": abs(
            shap_values.values
        ).mean(axis=0)

    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )

    st.subheader("🏆 Top Important Features")

    top3 = importance.head(3)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "🥇 Most Important",
            top3.iloc[0]["Feature"]
        )

    with c2:
        st.metric(
            "🥈 Second",
            top3.iloc[1]["Feature"]
        )

    with c3:
        st.metric(
            "🥉 Third",
            top3.iloc[2]["Feature"]
        )

    st.dataframe(
        importance,
        use_container_width=True
    )

    csv = importance.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Feature Importance",
        csv,
        "feature_importance.csv",
        "text/csv",
        use_container_width=True
    )

    st.markdown("---")

    # =====================================================
    # WATERFALL
    # =====================================================

    st.subheader("🔍 Explain Individual Prediction")

    row = st.slider(
        "Select Row",
        0,
        len(X)-1,
        0
    )

    fig = plt.figure(figsize=(10,6))

    shap.plots.waterfall(
        shap_values[row],
        show=False
    )

    st.pyplot(fig)

    plt.close()

    st.markdown("---")

    # =====================================================
    # AI INSIGHT
    # =====================================================

    top_feature = importance.iloc[0]["Feature"]

    st.info(f"""

## 🤖 AI Explanation

The machine learning model identified **{top_feature}** as the most influential feature.

### Business Interpretation

• This feature has the greatest impact on predictions.

• Monitoring this feature will improve business decisions.

• Improving data quality for this variable can increase model accuracy.

• Changes in this feature significantly influence business outcomes.

""")

st.markdown("---")

ai_insight(
    "Explainable AI increases transparency by identifying which features have the greatest influence on machine learning predictions."
)

page_footer()