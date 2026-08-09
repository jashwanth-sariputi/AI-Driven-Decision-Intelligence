import streamlit as st
from src.ui.layout import page_header, ai_insight, page_footer
from src.model_prediction.predictor import Predictor
from src.model_prediction.prediction_export import PredictionExporter
from src.model_prediction.prediction_visualizer import PredictionVisualizer
from src.database.database import Database

import pandas as pd
import os


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Prediction",
    page_icon="🔮",
    layout="wide"
)


# =========================================================
# PAGE HEADER
# =========================================================

page_header(
    "🔮 AI Prediction Engine",
    "Generate predictions using previously trained machine learning models."
)


# =========================================================
# FIND SAVED MODELS
# =========================================================

MODEL_FOLDER = "saved_models"

if not os.path.exists(MODEL_FOLDER):
    st.error("Saved models are currently unavailable.")
    st.stop()

models = [
    f for f in os.listdir(MODEL_FOLDER)
    if f.endswith(".pkl")
]

if len(models) == 0:
    st.warning("No trained prediction models are currently available.")
    st.stop()


# =========================================================
# SELECT MODEL
# =========================================================

selected_model = st.selectbox(
    "Select Model",
    models
)


# =========================================================
# UPLOAD DATASET
# =========================================================

uploaded_file = st.file_uploader(
    "Upload CSV for Prediction",
    type=["csv"]
)


if uploaded_file is not None:

    # -----------------------------------------------------
    # READ DATASET
    # -----------------------------------------------------

    try:
        df = pd.read_csv(uploaded_file)

    except Exception:
        st.error(
            "⚠️ We could not read this file. "
            "Please upload a valid CSV dataset."
        )
        st.stop()


    # -----------------------------------------------------
    # DISPLAY UPLOADED DATA
    # -----------------------------------------------------

    st.subheader("Uploaded Data")

    st.dataframe(
        df.head(),
        width="stretch"
    )


    # =====================================================
    # PREDICT BUTTON
    # =====================================================

    if st.button("🚀 Predict"):

        # -------------------------------------------------
        # LOAD MODEL
        # -------------------------------------------------

        try:

            predictor = Predictor(
                os.path.join(
                    MODEL_FOLDER,
                    selected_model
                )
            )

        except Exception:

            st.error(
                "⚠️ The selected prediction model could not be loaded. "
                "Please try another model."
            )

            st.stop()


        # =================================================
        # VALIDATE DATASET
        # =================================================

        try:

            missing, extra = predictor.validate_features(df)

        except Exception:

            st.error(
                "⚠️ The uploaded dataset could not be checked "
                "against the selected prediction model."
            )

            st.stop()


        # =================================================
        # DATASET NOT SUITABLE
        # =================================================

        if len(missing) > 0:

            st.warning(
                "⚠️ The uploaded dataset is not suitable for this "
                "prediction model. Please upload a compatible dataset "
                "to continue."
            )

            st.stop()


        # =================================================
        # EXTRA COLUMNS
        # =================================================

        if len(extra) > 0:

            st.info(
                "ℹ️ Some additional columns in the uploaded dataset "
                "are not required for this prediction and will be ignored."
            )

            df = df[predictor.feature_names]


        # =================================================
        # GENERATE PREDICTION
        # =================================================

        try:

            predictions = predictor.predict(df)

        except ValueError:

            st.warning(
                "⚠️ The uploaded dataset contains data that cannot "
                "be used with this prediction model. "
                "Please upload a compatible dataset to continue."
            )

            st.stop()

        except Exception:

            st.warning(
                "⚠️ We couldn't generate predictions from this dataset. "
                "Please check the dataset and try again."
            )

            st.stop()


        # =================================================
        # SUCCESS MESSAGE
        # =================================================

        st.success(
            "✅ Prediction completed successfully!"
        )


        # =================================================
        # DISPLAY PREDICTIONS
        # =================================================

        st.subheader("Prediction Results")

        st.dataframe(
            predictions,
            width="stretch"
        )


        # =================================================
        # CREATE RESULT DATASET
        # =================================================

        result = df.copy()

        result["Prediction"] = predictions


        # =================================================
        # SAVE PREDICTION HISTORY
        # =================================================

        try:

            database = Database()

            database.save_prediction(
                selected_model,
                uploaded_file.name,
                len(result)
            )

            st.success(
                "✅ Prediction saved successfully."
            )

        except Exception:

            st.info(
                "ℹ️ Prediction was generated, but the prediction "
                "history could not be saved."
            )


        # =================================================
        # PREDICTION HISTORY
        # =================================================

        try:

            st.write(
                "Current Prediction History:"
            )

            st.write(
                database.get_predictions()
            )

        except Exception:
            pass


        # =================================================
        # PREVIEW RESULT
        # =================================================

        st.subheader("Prediction Dataset")

        st.dataframe(
            result.head(),
            width="stretch"
        )


        # =================================================
        # EXPORT PREDICTIONS
        # =================================================

        try:

            exporter = PredictionExporter()

            filename = exporter.export_csv(
                result
            )

            with open(filename, "rb") as file:

                st.download_button(
                    "📥 Download Predictions",
                    file,
                    filename,
                    "text/csv"
                )

        except Exception:

            st.info(
                "ℹ️ Predictions were generated successfully, "
                "but the download file could not be created."
            )


        # =================================================
        # PREDICTION VISUALIZATION
        # =================================================

        try:

            visualizer = PredictionVisualizer()

            st.subheader(
                "📊 Prediction Distribution"
            )


            # ---------------------------------------------
            # Histogram
            # ---------------------------------------------

            fig = visualizer.histogram(
                result,
                "Prediction"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )


            # ---------------------------------------------
            # Bar Chart
            # ---------------------------------------------

            fig = visualizer.bar(
                result,
                "Prediction"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )


            # ---------------------------------------------
            # Pie Chart
            # ---------------------------------------------

            fig = visualizer.pie(
                result,
                "Prediction"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        except Exception:

            st.info(
                "ℹ️ Prediction was completed, but the "
                "visualization could not be generated."
            )


        # =================================================
        # AI INSIGHT
        # =================================================

        ai_insight(
            "Always use prediction datasets that contain the "
            "same features used during model training."
        )


# =========================================================
# PAGE FOOTER
# =========================================================

page_footer()