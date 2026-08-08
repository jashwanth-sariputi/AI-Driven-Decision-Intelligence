import streamlit as st
import pandas as pd
import os

from src.model_prediction.predictor import Predictor
from src.model_prediction.prediction_visualizer import PredictionVisualizer
from src.ui.layout import page_header, ai_insight, page_footer

st.set_page_config(
    page_title="AI Predictor",
    page_icon="🎯",
    layout="wide"
)

page_header(
    "🎯 AI Predictor",
    "Generate predictions using trained machine learning models."
)

# --------------------------------------------------
# Load Saved Models
# --------------------------------------------------

model_folder = "saved_models"

if not os.path.exists(model_folder):
    st.warning("No saved models found.")
    st.stop()

models = [
    file
    for file in os.listdir(model_folder)
    if file.endswith(".pkl")
]

if len(models) == 0:
    st.warning("No trained models available.")
    st.stop()

selected_model = st.selectbox(
    "Choose Model",
    models
)

# --------------------------------------------------
# Upload Dataset
# --------------------------------------------------

uploaded = st.file_uploader(
    "Upload Prediction Dataset",
    type=["csv"]
)

if uploaded is not None:

    with st.spinner("Generating prediction..."):

        predictions = model.predict(X)

    st.subheader("📄 Prediction Dataset")

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    if st.button("🚀 Predict"):

      with st.spinner("🤖 Generating AI Predictions..."):

        predictor = Predictor(
            os.path.join(
            model_folder,
            selected_model
            )
        )

    # rest of prediction code
        

        try:

            prediction = predictor.predict(df)

            result = df.copy()

            result["Prediction"] = prediction

            # -------------------------------------
            # Success Message
            # -------------------------------------

            st.success("✅ Prediction Completed Successfully")

            # -------------------------------------
            # Summary
            # -------------------------------------

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
                    selected_model.replace(".pkl", "")
                )

            st.markdown("---")

            # -------------------------------------
            # Results
            # -------------------------------------
            st.divider()
            st.subheader("📋 Prediction Results")

            with st.expander("📋 View Prediction Results", expanded=True):

                st.dataframe(
                    result,
                    use_container_width=True
                )

            # -------------------------------------
            # Download
            # -------------------------------------

            csv = result.to_csv(index=False).encode("utf-8")
            st.subheader("⬇ Export Predictions")

            st.download_button(
                "📥 Download Predictions",
                data=csv,
                file_name="predictions.csv",
                mime="text/csv"
            )
            

            # -------------------------------------
            # Prediction Analytics
            # -------------------------------------

            st.markdown("---")

            st.subheader("📊 Prediction Analytics")

            visualizer = PredictionVisualizer()

            fig = visualizer.histogram(
                result,
                "Prediction"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            fig = visualizer.bar(
                result,
                "Prediction"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            fig = visualizer.pie(
                result,
                "Prediction"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except ValueError:

            st.error("❌ Incompatible Dataset")

            st.warning("""
The uploaded dataset is not compatible with the selected AI model.

Please ensure:

• You selected the correct trained model.

• The uploaded dataset belongs to the same business domain.

• All required columns are present.
            """)

            missing, extra = predictor.validate_features(df)

            if len(missing) > 0:

                st.subheader("❌ Missing Columns")

                st.dataframe(
                    pd.DataFrame(
                        {
                            "Required Columns": missing
                        }
                    ),
                    use_container_width=True
                )

            if len(extra) > 0:

                st.subheader("⚠ Extra Columns")

                st.dataframe(
                    pd.DataFrame(
                        {
                            "Extra Columns": extra
                        }
                    ),
                    use_container_width=True
                )

            st.info(
                "💡 Upload the same dataset used for model training."
            )

        except Exception as e:

            st.error("❌ Prediction Failed")

            st.info(
                "An unexpected error occurred while generating predictions."
            )

            st.caption(str(e))
        ai_insight(
            "AI Prediction estimates future outcomes using previously trained machine learning models."
        )

page_footer()