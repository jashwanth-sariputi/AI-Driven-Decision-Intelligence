import streamlit as st
from src.ui.layout import page_header, ai_insight, page_footer
from src.ui.status import loading, success
import pandas as pd
import os

from src.model_prediction.predictor import Predictor
from src.model_prediction.prediction_export import PredictionExporter
from src.model_prediction.prediction_visualizer import PredictionVisualizer
from src.database.database import Database

st.set_page_config(
    page_title="AI Prediction",
    page_icon="🔮",
    layout="wide"
)

page_header(
    "🔮 AI Prediction Engine",
    "Generate predictions using previously trained machine learning models."
)

# -----------------------------
# Find Saved Models
# -----------------------------

MODEL_FOLDER = "saved_models"

if not os.path.exists(MODEL_FOLDER):
    st.error("saved_models folder not found.")
    st.stop()

models = [f for f in os.listdir(MODEL_FOLDER) if f.endswith(".pkl")]

if len(models) == 0:
    st.warning("No trained models found.")
    st.stop()

selected_model = st.selectbox(
    "Select Model",
    models
)

uploaded_file = st.file_uploader(
    "Upload CSV for Prediction",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Data")

    st.dataframe(df.head())

if st.button("🚀 Predict"):

    predictor = Predictor(
        os.path.join(
            MODEL_FOLDER,
            selected_model
        )
    )

    # ------------------------------------
    # Validate Dataset
    # ------------------------------------

    missing, extra = predictor.validate_features(df)

    if len(missing) > 0:

        st.error("❌ Dataset is not compatible with this model.")

        st.subheader("Missing Columns")

        st.write(missing)

        st.stop()

    if len(extra) > 0:

        st.warning("⚠ Extra columns detected.")

        st.write(extra)

        st.info("Extra columns will be ignored.")

        df = df[predictor.feature_names]

    # ------------------------------------
    # Prediction
    # ------------------------------------

    try:

        predictions = predictor.predict(df)

    except Exception as e:

        st.error("Prediction failed.")

        st.exception(e)

        st.stop()

    result = df.copy()

    result["Prediction"] = predictions

    database = Database()

    database.save_prediction(
        selected_model,
        uploaded_file.name,
        len(result)
    )

    st.success("✅ Prediction saved")

    st.write("Current Prediction History:")
    st.write(database.get_predictions())
    

    st.dataframe(result.head())

    exporter = PredictionExporter()

    filename = exporter.export_csv(result)

    with open(filename, "rb") as file:

        st.download_button(
            "📥 Download Predictions",
            file,
            filename,
            "text/csv"
        )

    visualizer = PredictionVisualizer()

    st.subheader("Prediction Distribution")

    fig = visualizer.histogram(
        result,
        "Prediction"
    )

    st.plotly_chart(fig, width="stretch")

    fig = visualizer.bar(
        result,
        "Prediction"
    )

    st.plotly_chart(fig, width="stretch")

    fig = visualizer.pie(
        result,
        "Prediction"
    )

    st.plotly_chart(fig, width="stretch")
    ai_insight(
        "Always use prediction datasets that contain the same features used during model training."
        )
    page_footer()