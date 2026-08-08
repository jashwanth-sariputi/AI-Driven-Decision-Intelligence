import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.forecasting.forecast_engine import ForecastEngine
from src.ui.layout import page_header, ai_insight, page_footer

st.set_page_config(
    page_title="Business Forecasting",
    page_icon="📈",
    layout="wide"
)

page_header(
    "📈 AI Business Forecasting",
    "Forecast future business trends using Artificial Intelligence."
)

# =====================================================
# CHECK DATASET
# =====================================================

if "dataset" not in st.session_state:

    st.warning("Please upload a dataset first.")

    st.stop()

df = st.session_state["dataset"]

numeric_columns = list(df.select_dtypes(include="number").columns)

if len(numeric_columns) == 0:

    st.error("No numeric columns available for forecasting.")

    st.stop()

# =====================================================
# USER INPUT
# =====================================================

target = st.selectbox(
    "Select Numeric Column",
    numeric_columns
)

periods = st.slider(
    "Forecast Future Periods",
    min_value=5,
    max_value=100,
    value=30
)

st.markdown("---")

# =====================================================
# FORECAST
# =====================================================

if st.button(
    "🚀 Generate Forecast",
    use_container_width=True
):

    try:

        with st.spinner("Generating AI Forecast..."):

            engine = ForecastEngine()

            with st.spinner("Forecasting future values..."):

                prediction = engine.forecast(
                    df,
                    target,
                    periods
                )

        st.success("✅ Forecast Generated Successfully")

        history = df[target].dropna().reset_index(drop=True)

        historical = pd.DataFrame({

            "Time": range(len(history)),
            "Value": history,
            "Type": "Historical"

        })

        future = pd.DataFrame({

            "Time": range(
                len(history),
                len(history) + periods
            ),

            "Value": prediction,
            "Type": "Forecast"

        })

        final = pd.concat(
            [historical, future],
            ignore_index=True
        )

        # =====================================================
        # KPI DASHBOARD
        # =====================================================

        st.markdown("---")

        st.subheader("📊 Forecast Summary")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Historical Rows",
                len(history)
            )

        with c2:
            st.metric(
                "Forecast Periods",
                periods
            )

        with c3:
            st.metric(
                "Current Value",
                round(history.iloc[-1], 2)
            )

        with c4:
            st.metric(
                "Forecast End",
                round(prediction[-1], 2)
            )

        st.markdown("---")

        # =====================================================
        # LINE CHART
        # =====================================================

        st.subheader("📈 Historical vs Forecast")

        fig = px.line(
            final,
            x="Time",
            y="Value",
            color="Type",
            markers=True,
            title="Business Forecast"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =====================================================
        # FORECAST TABLE
        # =====================================================

        st.subheader("📋 Forecast Results")

        st.dataframe(
            future,
            use_container_width=True
        )

        # =====================================================
        # FORECAST STATISTICS
        # =====================================================

        st.subheader("📊 Forecast Statistics")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Minimum",
                round(future["Value"].min(), 2)
            )

        with c2:
            st.metric(
                "Average",
                round(future["Value"].mean(), 2)
            )

        with c3:
            st.metric(
                "Maximum",
                round(future["Value"].max(), 2)
            )

        st.markdown("---")

        # =====================================================
        # AI INSIGHT
        # =====================================================

        trend = "Increasing 📈"

        if prediction[-1] < history.iloc[-1]:
            trend = "Decreasing 📉"

        st.subheader("🤖 AI Forecast Insight")

        st.info(f"""

### Forecast Analysis

• Forecast Target : **{target}**

• Forecast Horizon : **{periods} periods**

• Expected Trend : **{trend}**

• Current Value : **{round(history.iloc[-1],2)}**

• Final Forecast : **{round(prediction[-1],2)}**

### Recommendation

Monitor this KPI regularly and compare actual values with forecasted values to improve business planning.

""")

        # =====================================================
        # DOWNLOAD
        # =====================================================

        csv = future.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download Forecast CSV",
            csv,
            "forecast.csv",
            "text/csv",
            use_container_width=True
        )

    except Exception:

        st.error("❌ Forecast generation failed.")

        st.info(
            "Please ensure the selected column contains valid numeric data."
        )

st.markdown("---")

ai_insight(
    "Business forecasting enables organizations to anticipate future trends, optimize resources, reduce risks, and make proactive strategic decisions."
)

page_footer()