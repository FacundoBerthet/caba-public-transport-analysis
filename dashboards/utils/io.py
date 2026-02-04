import streamlit as st
from pathlib import Path
import geopandas as gpd

def get_processed_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "processed"


@st.cache_data
def load_data():
    """Load processed geospatial datasets from data/processed."""
    base_path = get_processed_path()

    paradas = gpd.read_file(base_path / "stops.gpkg")
    calles = gpd.read_file(base_path / "calles.gpkg")
    comunas = gpd.read_file(base_path / "comunas.gpkg")
    barrios = gpd.read_file(base_path / "barrios.gpkg")

    return paradas, calles, comunas, barrios
