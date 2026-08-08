import streamlit as st


from src.kpi_dashboard.kpi_engine import KPIEngine
from src.ui.layout import page_header, ai_insight, page_footer

st.set_page_config(

    page_title="KPI Dashboard",

    page_icon="📊",

    layout="wide"

)

page_header(
    "📈 KPI Dashboard",
    "Monitor key business performance indicators."
)

if "dataset" not in st.session_state:

    st.warning("Upload a dataset first.")

    st.stop()

df = st.session_state["dataset"]

engine = KPIEngine()

kpis = engine.generate(df)

if kpis is None:

    st.error("No numeric columns found.")

    st.stop()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", kpis["Rows"])

col2.metric("Columns", kpis["Columns"])

col3.metric("Numeric Columns", kpis["Numeric Columns"])

col4.metric("Missing Values", kpis["Missing Values"])

st.divider()

col5, col6, col7, col8 = st.columns(4)

col5.metric("Average", kpis["Average"])

col6.metric("Maximum", kpis["Maximum"])

col7.metric("Minimum", kpis["Minimum"])

col8.metric("Total Sum", kpis["Total Sum"])
ai_insight(
    "KPIs measure organizational performance and help monitor business success."
)

page_footer()