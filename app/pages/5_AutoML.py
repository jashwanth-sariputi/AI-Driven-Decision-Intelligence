import streamlit as st
from src.ui.layout import page_header, ai_insight, page_footer
from src.ui.status import loading, success

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from src.automl.automl_engine import AutoMLEngine
from src.database.database import Database
from src.model_recommendation.model_recommender import ModelRecommender
from src.model_export.model_exporter import ModelExporter

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI AutoML Engine",
    page_icon="🤖",
    layout="wide"
)

page_header(
    "🤖 AI AutoML Engine",
    "Automatically train, compare and recommend the best Machine Learning model."
)

# --------------------------------------------------
# CHECK DATASET
# --------------------------------------------------

if "dataset" not in st.session_state:

    st.warning("⚠ Please upload a dataset first.")

    st.stop()

df = st.session_state["dataset"]

st.success("✅ Dataset Loaded Successfully")

# --------------------------------------------------
# DATASET OVERVIEW
# --------------------------------------------------

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
# TARGET COLUMN
# --------------------------------------------------

ignore_columns = [
    "order_id",
    "customer_id",
    "product_id",
    "seller_id",
    "row id",
    "row_id",
    "id"
]

target_columns = [
    c for c in df.columns
    if c.lower() not in ignore_columns
]

target = st.selectbox(
    "🎯 Prediction Target",
    target_columns
)

# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------

if st.button("🚀 Train Model"):

    with st.spinner("🤖 Training AI Model..."):

        data = df.copy()

        # ----------------------------------------
        # Remove Missing Values
        # ----------------------------------------

        data = data.dropna().reset_index(drop=True)

        if len(data) > 15000:

            data = data.sample(
                15000,
                random_state=42
            )

            st.info(
                "Large dataset detected. Training on a random sample of 15,000 rows."
            )

        # ----------------------------------------
        # Remove Constant Columns
        # ----------------------------------------

        constant_cols = [
            c
            for c in data.columns
            if data[c].nunique() <= 1
        ]

        data.drop(
            columns=constant_cols,
            inplace=True,
            errors="ignore"
        )

        if target not in data.columns:

            st.error("Target column was removed during preprocessing.")

            st.stop()

        # ----------------------------------------
        # Encode Features
        # ----------------------------------------

        for col in data.columns:

            if col == target:
                continue

            try:

                dt = pd.to_datetime(
                    data[col],
                    errors="raise"
                )

                data[col] = dt.astype("int64") // 10**9

                continue

            except Exception:

                pass

            if not pd.api.types.is_numeric_dtype(data[col]):

                encoder = LabelEncoder()

                data[col] = encoder.fit_transform(
                    data[col].astype(str)
                )

        # ----------------------------------------
        # Encode Target
        # ----------------------------------------

        if not pd.api.types.is_numeric_dtype(data[target]):

            encoder = LabelEncoder()

            data[target] = encoder.fit_transform(
                data[target].astype(str)
            )

        # ----------------------------------------
        # Split Dataset
        # ----------------------------------------

        X = data.drop(columns=[target])

        y = data[target]

        object_columns = X.select_dtypes(
            include=["object"]
        ).columns

        if len(object_columns) > 0:

            st.error(
                f"Object columns still exist: {list(object_columns)}"
            )

            st.stop()

        X_train, X_test, y_train, y_test = train_test_split(

            X,
            y,

            test_size=0.20,

            random_state=42

        )

        # ----------------------------------------
        # AutoML Training
        # ----------------------------------------

        automl = AutoMLEngine()

        status = st.empty()

        progress = st.progress(0)

        status.info("🔄 Preparing AI Engine...")

        progress.progress(10)

        with loading("🤖 Comparing Machine Learning Models..."):

            status.info("⚙️ Training models...")

            progress.progress(30)

            results = automl.compare_models(

                X_train,
                X_test,
                y_train,
                y_test

            )

            status.info("📊 Evaluating performance...")

            progress.progress(70)

            best_model = max(results, key=results.get)

            status.info("🏆 Selecting Best Model...")

            progress.progress(90)

        progress.progress(100)

        status.success("✅ AutoML Completed Successfully!")

        st.toast("🎉 AI Training Completed!")

        st.balloons()
                # ----------------------------------------
        # MODEL COMPARISON
        # ----------------------------------------

        st.subheader("🏆 Model Comparison")

        results_df = pd.DataFrame({

            "Model": list(results.keys()),
            "Score": list(results.values())

        })

        st.dataframe(
            results_df,
            use_container_width=True
        )

        # ----------------------------------------
        # BEST MODEL
        # ----------------------------------------

        best_model = max(results, key=results.get)

        st.success(
            f"🥇 Best Model Selected: **{best_model}**"
        )

        # ----------------------------------------
        # EXPORT MODEL
        # ----------------------------------------

        exporter = ModelExporter()

        filepath = exporter.export(

            model=automl.best_model,

            model_name=best_model.replace(" ", "_"),

            feature_names=list(X.columns),

            target_column=target,

            problem_type=automl.problem_type

        )

        success("✅ Best model exported successfully.")

        # ----------------------------------------
        # SAVE MODEL HISTORY
        # ----------------------------------------

        database = Database()

        dataset_name = st.session_state.get(
            "filename",
            "Uploaded Dataset"
        )

        database.save_model(

            dataset_name,

            best_model,

            results[best_model],

            automl.problem_type

        )

        # ----------------------------------------
        # TRAINING SUMMARY
        # ----------------------------------------

        st.subheader("📋 Training Summary")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Best Model",
                best_model
            )

        with c2:

            if automl.problem_type == "classification":

                st.metric(
                    "Accuracy",
                    f"{results[best_model]:.2f}%"
                )

            else:

                st.metric(
                    "R² Score",
                    f"{results[best_model]:.2f}"
                )

        with c3:
            st.metric(
                "Problem Type",
                automl.problem_type.title()
            )

        with c4:
            st.metric(
                "Features",
                len(X.columns)
            )

        st.divider()

        # ----------------------------------------
        # AI RECOMMENDATIONS
        # ----------------------------------------

        recommender = ModelRecommender()

        recommendations = recommender.recommend(

            best_model,

            results[best_model],

            automl.problem_type

        )

        st.subheader("🤖 AI Recommendations")

        for recommendation in recommendations:

            st.success(recommendation)

        st.divider()

        # ----------------------------------------
        # FEATURE IMPORTANCE
        # ----------------------------------------

        importance = automl.feature_importance(

            X.columns

        )

        if importance is not None:

            st.subheader("📊 Feature Importance")

            imp_df = pd.DataFrame({

                "Feature": list(importance.keys()),

                "Importance": list(importance.values())

            })

            imp_df = imp_df.sort_values(

                by="Importance",

                ascending=False

            )

            st.dataframe(
                imp_df,
                use_container_width=True
            )

            st.bar_chart(

                imp_df.set_index("Feature")

            )

        else:

            st.info(
                "Feature importance is not available for this model."
            )

        st.divider()

        # ----------------------------------------
        # AI INSIGHT
        # ----------------------------------------

        ai_insight(

            "The AI engine automatically compared multiple machine learning algorithms and selected the highest-performing model. Review the feature importance before deploying the model into production."

        )

        page_footer()