import geopandas as gpd

def add_area_km2(gdf: gpd.GeoDataFrame, area_col: str = "area") -> gpd.GeoDataFrame:
    res = gdf.copy()
    res["area_km2"] = res[area_col] / 1_000_000
    return res

def add_stop_counts(
    gdf: gpd.GeoDataFrame,
    stops: gpd.GeoDataFrame,
    group_col: str,
    out_col: str = "n_stops",
) -> gpd.GeoDataFrame:
    counts = stops.groupby(group_col).size().rename(out_col).reset_index()
    res = gdf.merge(counts, on=group_col, how="left")
    res[out_col] = res[out_col].fillna(0).astype(int)
    return res

def add_density(
    gdf: gpd.GeoDataFrame,
    count_col: str = "n_stops",
    area_col: str = "area_km2",
    out_col: str = "stops_per_km2",
) -> gpd.GeoDataFrame:
    res = gdf.copy()
    res[out_col] = res[count_col] / res[area_col]
    return res