import streamlit as st
import geopandas as gpd

from utils.io import load_data
from utils.metrics import add_area_km2


# Page config
st.set_page_config(
    page_title="Overview",
    page_icon="🚌",
    layout="wide"
)

# Load data
stops, calles, comunas, barrios = load_data()

# Add area in km²
comunas = add_area_km2(comunas)
barrios = add_area_km2(barrios)

st.title("Overview")

st.markdown("""
En esta sección se presenta una **vista general de los conjuntos de datos** utilizados en el análisis. El objetivo es ofrecer un primer contexto antes de profundizar en mapas y métricas más específicas.
""")

st.subheader("Indicadores generales")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de paradas", stops.shape[0])
with col2:
    st.metric("Total de comunas", comunas.shape[0])
with col3:
    st.metric("Total de barrios", barrios.shape[0])
with col4: 
    total_area = comunas["area_km2"].sum()
    st.metric("Area CABA", f"{total_area:.1f} km²")