import geopandas as gpd

def add_area_km2(gdf: gpd.GeoDataFrame, area_col: str = "area") -> gpd.GeoDataFrame:
    res = gdf.copy()
    res["area_km2"] = res[area_col] / 1_000_000
    return res
