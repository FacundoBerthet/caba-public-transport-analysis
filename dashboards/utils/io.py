from pathlib import Path
import geopandas as gpd

def get_processed_path() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "processed"

def load_ds():
    """Load processed geospatial datasets from data/processed."""
    base_path = get_processed_path()

    paradas = gpd.read_file(base_path / "stops.gpkg")
    calles = gpd.read_file(base_path / "calles.gpkg")
    comunas = gpd.read_file(base_path / "comunas.gpkg")
    barrios = gpd.read_file(base_path / "barrios.gpkg")

    return paradas, calles, comunas, barrios
