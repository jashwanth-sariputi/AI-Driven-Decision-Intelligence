import streamlit as st
import pandas as pd
import os

from src.model_prediction.predictor import Predictor
from src.model_prediction.prediction_visualizer import PredictionVisualizer
from src.ui.layout import page_header, ai_insight, page_footer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Predictor",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# PAGE HEADER
# ============================================================

page_header(
    "🎯 AI Predictor",
    "Generate predictions using trained machine learning models."
)


# ============================================================
# LOAD SAVED MODELS
# ============================================================

model_folder = "saved_models"

if not os.path.exists(model_folder):

    st.warning(
        "⚠️ No trained models are available yet. "
        "Please train a model before generating predictions."
    )

    page_footer()
    st.stop()


models = [
    file
    for file in os.listdir(model_folder)
    if file.endswith(".pkl")
]


if len(models) == 0:

    st.warning(
        "⚠️ No trained machine learning models were found. "
        "Please train a model first."
    )

    page_footer()
    st.stop()


# ============================================================
# MODEL SELECTION
# ============================================================

selected_model = st.selectbox(
    "Choose Model",
    models
)


# ============================================================
# UPLOAD DATASET
# ============================================================

uploaded = st.file_uploader(
    "Upload Prediction Dataset",
    type=["csv"]
)


if uploaded is not None:

    # --------------------------------------------------------
    # READ DATASET
    # --------------------------------------------------------

    try:

        df = pd.read_csv(uploaded)

    except Exception:

        st.error(
            "⚠️ We couldn't read this file. "
            "Please upload a valid CSV dataset."
        )

        page_footer()
        st.stop()


    # --------------------------------------------------------
    # UPLOAD SUCCESS MESSAGE
    # --------------------------------------------------------

    st.success(
        "✅ Dataset uploaded successfully. "
        "Review the data below and click **Predict** to generate AI predictions."
    )


    # --------------------------------------------------------
    # DATASET PREVIEW
    # --------------------------------------------------------

    st.subheader("📄 Uploaded Prediction Data")

    st.dataframe(
        df.head(),
        use_container_width=True
    )


    st.caption(
        f"Showing the first 5 rows of {len(df):,} uploaded records."
    )


    # ========================================================
    # PREDICT BUTTON
    # ========================================================

    if st.button(
        "🚀 Predict",
        use_container_width=False
    ):

        with st.spinner("🤖 Generating AI predictions..."):

            try:

                # ------------------------------------------------
                # LOAD SELECTED MODEL
                # ------------------------------------------------

                predictor = Predictor(
                    os.path.join(
                        model_folder,
                        selected_model
                    )
                )


                # ------------------------------------------------
                # VALIDATE DATASET FEATURES
                # ------------------------------------------------

                missing, extra = predictor.validate_features(df)


                # ------------------------------------------------
                # MISSING REQUIRED COLUMNS
                # ------------------------------------------------

                if len(missing) > 0:

                    st.warning(
                        "⚠️ This dataset is not suitable for the "
                        "selected prediction model. "
                        "Please upload a dataset containing the "
                        "required prediction features."
                    )

                    st.info(
                        "💡 Please choose the correct model or "
                        "upload a dataset from the same business domain "
                        "used during model training."
                    )

                    st.stop()


                # ------------------------------------------------
                # REMOVE EXTRA COLUMNS
                # ------------------------------------------------

                if len(extra) > 0:

                    st.info(
                        "ℹ️ Some additional columns were found in the "
                        "uploaded dataset. They will not be used for prediction."
                    )

                    df_prediction = df[
                        predictor.feature_names
                    ]

                else:

                    df_prediction = df[
                        predictor.feature_names
                    ]


                # ------------------------------------------------
                # GENERATE PREDICTIONS
                # ------------------------------------------------

                predictions = predictor.predict(
                    df_prediction
                )


                # ------------------------------------------------
                # CREATE RESULT DATAFRAME
                # ------------------------------------------------

                result = df.copy()

                result["Prediction"] = predictions


                # =================================================
                # SUCCESS MESSAGE
                # =================================================

                st.success(
                    "🎉 Predictions generated successfully!"
                )


                # =================================================
                # PREDICTION SUMMARY
                # =================================================

                st.subheader("📈 Prediction Summary")

                c1, c2, c3 = st.columns(3)


                with c1:

                    st.metric(
                        "Rows Predicted",
                        len(result)
                    )


                with c2:

                    st.metric(
                        "Features Used",
                        len(predictor.feature_names)
                    )


                with c3:

                    st.metric(
                        "Model",
                        selected_model.replace(
                            ".pkl",
                            ""
                        )
                    )


                st.divider()


                # =================================================
                # PREDICTION RESULTS
                # =================================================

                st.subheader("📋 Prediction Results")

                with st.expander(
                    "📋 View Prediction Results",
                    expanded=True
                ):

                    st.dataframe(
                        result,
                        use_container_width=True
                    )


                # =================================================
                # DOWNLOAD PREDICTIONS
                # =================================================

                st.subheader("⬇️ Export Predictions")

                csv = result.to_csv(
                    index=False
                ).encode("utf-8")


                st.download_button(
                    "📥 Download Predictions",
                    data=csv,
                    file_name="predictions.csv",
                    mime="text/csv"
                )


                # =================================================
                # PREDICTION ANALYTICS
                # =================================================

                st.divider()

                st.subheader(
                    "📊 Prediction Analytics"
                )


                visualizer = PredictionVisualizer()


                # ------------------------------------------------
                # HISTOGRAM
                # ------------------------------------------------

                try:

                    fig = visualizer.histogram(
                        result,
                        "Prediction"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                except Exception:

                    st.info(
                        "ℹ️ Prediction distribution chart "
                        "is not available for this model output."
                    )


                # ------------------------------------------------
                # BAR CHART
                # ------------------------------------------------

                try:

                    fig = visualizer.bar(
                        result,
                        "Prediction"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                except Exception:

                    pass


                # ------------------------------------------------
                # PIE CHART
                # ------------------------------------------------

                try:

                    fig = visualizer.pie(
                        result,
                        "Prediction"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                except Exception:

                    pass


            # ====================================================
            # USER-FRIENDLY DATA ERROR
            # ====================================================

            except ValueError:

                st.warning(
                    "⚠️ We couldn't generate predictions from this dataset."
                )

                st.info(
                    "Please upload a dataset that contains the "
                    "same type of information used when training "
                    "the selected AI model."
                )


            # ====================================================
            # OTHER ERRORS
            # ====================================================

            except Exception:

                st.warning(
                    "⚠️ We couldn't generate predictions for this dataset."
                )

                st.info(
                    "Please check that the selected model matches "
                    "the uploaded dataset and try again."
                )


    # ========================================================
    # AI INSIGHT
    # ========================================================

    ai_insight(
        "AI Prediction estimates outcomes using previously "
        "trained machine learning models."
    )


# ============================================================
# FOOTER
# ============================================================

page_footer()