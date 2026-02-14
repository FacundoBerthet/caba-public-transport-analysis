import streamlit as st
import geopandas as gpd
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

from utils.io import load_data
from utils.metrics import *


# Page config
st.set_page_config(
    page_title="Lines & Coverage",
    page_icon="🚌",
    layout="wide"
)

# Load data
stops, calles, comunas, barrios = load_data()

# Add area in km²
comunas = add_area_km2(comunas)
barrios = add_area_km2(barrios)


st.title("Líneas y Cobertura")

st.markdown("""
En esta sección se analiza la **diversidad de líneas de colectivo** que sirven diferentes 
áreas de la ciudad.
""")

# Center for maps
minx, miny, maxx, maxy = comunas.total_bounds
center = {"lon": (minx + maxx) / 2, "lat": (miny + maxy) / 2}


# === Prepare line data ===
line_cols = ["l1", "l2", "l3", "l4", "l5", "l6"]

# Long format: one row per (stop, line)
stops_lines = (
    stops[["comuna", "barrio"] + line_cols]
    .melt(id_vars=["comuna", "barrio"], value_vars=line_cols, value_name="line")
    .dropna(subset=["line"])
)
stops_lines["line"] = stops_lines["line"].astype(int)

lines_by_stops = (
    stops_lines.groupby("line")
    .size()
    .rename("n_stops")
    .sort_values(ascending=False)
    .reset_index()
)
lines_by_stops["line"] = lines_by_stops["line"].astype(str)


# === General metrics ====
st.subheader("Indicadores generales")

total_lines = stops_lines["line"].nunique()
total_stops = len(stops)
avg_lines_per_stop = stops["n_lines"].mean()
avg_stops_per_line = lines_by_stops["n_stops"].mean()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de líneas", f"{total_lines:,}")
with col2:
    st.metric("Total de paradas", f"{total_stops:,}")
with col3:
    st.metric("Promedio líneas/parada", f"{avg_lines_per_stop:.1f}")
with col4:
    st.metric("Promedio paradas/línea", f"{avg_stops_per_line:.1f}")




# === Lines with most stops ===
st.header("Líneas con Mayor Cobertura")

st.markdown("""
Las líneas con más paradas generalmente tienen rutas más largas o ramales múltiples, 
atravesando diferentes zonas de la ciudad.
""")

col1, col2 = st.columns(2)

with col1:
    top_n_lines = st.slider("Seleccionar Top N líneas", 5, 30, 15, key="lines_slider")

with col2:
    st.write("")  

fig = px.bar(
    lines_by_stops.head(top_n_lines),
    x="n_stops",
    y="line",
    orientation="h",
    title=f"Top {top_n_lines} Líneas por Número de Paradas",
    labels={"n_stops": "Número de Paradas", "line": "Línea"}
)
fig.update_traces(
    hovertemplate=(
        "<b>Línea %{y}</b><br>"
        "Paradas: %{x:,}"
        "<extra></extra>"
    ),
    marker_line_color="grey",
    marker_line_width=1
)
fig.update_yaxes(type="category") 
fig.update_xaxes(showgrid=True, gridwidth=1)
fig.update_layout(height=700, yaxis={"categoryorder": "total ascending"}, bargap=0.25)
st.plotly_chart(fig, use_container_width=True)



# === Lines by Comuna ===
st.header("Diversidad de Líneas por Comuna")

st.markdown("""
Este análisis muestra cuántas líneas **distintas** sirven cada comuna, 
capturando la diversidad de rutas más que el volumen de paradas.
""")

lines_by_comuna = (
    stops_lines
    .groupby("comuna")["line"]
    .nunique()
    .rename("n_lines")
    .sort_values(ascending=False)
    .reset_index()
)

# Merge with comunas geodataframe
comunas_lines = comunas.merge(lines_by_comuna, on="comuna", how="left")
comunas_lines["n_lines"] = comunas_lines["n_lines"].fillna(0).astype(int)

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        comunas_lines,
        x="n_lines",
        y="comuna",
        orientation="h",
        title="Número de Líneas Distintas por Comuna",
        labels={"n_lines": "Número de Líneas Distintas", "comuna": "Comuna"}
    )
    fig.update_traces(
    hovertemplate=(
        "<b>Comuna %{y}</b><br>"
        "Líneas distintas: %{x:,}"
        "<extra></extra>"
    ),
    marker_line_color="grey",
    marker_line_width=1
)
    fig.update_layout(yaxis=dict(type="category", categoryorder="total ascending"), height=600)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.choropleth_mapbox(
        comunas_lines,
        geojson=comunas_lines.__geo_interface__,
        locations=comunas_lines.index,
        color="n_lines",
        hover_name="comuna",
        hover_data={"n_lines": True},  # agregá n_stops sólo si existe
        mapbox_style="carto-positron",
        center=center,
        zoom=10.4,
        opacity=0.6,
        color_continuous_scale="Greens",
        title="Mapa de Diversidad de Líneas por Comuna"
    )
    fig.update_traces(
    hovertemplate=(
        "<b>Comuna %{hovertext}</b><br>"
        "Líneas distintas: %{z:,}"
        "<extra></extra>"
        )
    )
    fig.update_layout(height=600, margin={"r": 0, "t": 70, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)


# === Lines by Barrio ===
st.header("Diversidad de Líneas por Barrio")

stops_by_barrio = (
    stops.groupby("barrio")
    .size()
    .rename("n_stops")
    .reset_index()
)

lines_by_barrio = (
    stops_lines
    .groupby("barrio")["line"]
    .nunique()
    .rename("n_lines")
    .sort_values(ascending=False)
    .reset_index()
)

# Merge with barrios geodataframe
barrios_lines = barrios.merge(lines_by_barrio, left_on="barrio", right_on="barrio", how="left")
barrios_lines["n_lines"] = barrios_lines["n_lines"].fillna(0).astype(int)
barrios_lines = barrios_lines.drop(columns=["n_stops"], errors="ignore").merge(
    stops_by_barrio,
    on="barrio",
    how="left"
)

col1, col2 = st.columns(2)
with col1:
    top_n_barrios = st.slider("Seleccionar Top N barrios", 5, 48, 15, key="barrios_lines_slider")

with col2:
    st.write("")  # Spacer

# Bar chart
fig = px.bar(
    barrios_lines.sort_values("n_lines", ascending=False).head(top_n_barrios),
    x="n_lines",
    y="barrio",
    orientation="h",
    title=f"Top {top_n_barrios} Barrios por Número de Líneas Distintas",
    labels={"n_lines": "Número de Líneas Distintas", "barrio": "Barrio"}
)
fig.update_traces(
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Líneas distintas: %{x:,}"
        "<extra></extra>"
    ),
    marker_line_color="grey",
    marker_line_width=1
)
fig.update_layout(
    height=700,
    yaxis={'categoryorder': 'total ascending'}
)
fig.update_xaxes(showgrid=True, gridwidth=1)
st.plotly_chart(fig, use_container_width=True)

barrios_lines["n_stops"] = barrios_lines.get("n_stops", 0)
barrios_lines["n_stops"] = barrios_lines["n_stops"].fillna(0).astype(int)

#map
fig = px.choropleth_mapbox(
    barrios_lines,
    geojson=barrios_lines.__geo_interface__,
    locations=barrios_lines.index,
    color="n_lines",
    hover_name="barrio",
    custom_data=["n_stops"],
    mapbox_style="carto-positron",
    center=center,
    zoom=10.6,
    opacity=0.6,
    color_continuous_scale="Greens",
    title="Mapa de Diversidad de Líneas por Barrio"
)
fig.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "Líneas distintas: %{z:,}<br>"
        "Paradas: %{customdata[0]:,}"
        "<extra></extra>"
    )
)
fig.update_layout(
    height=600,
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    coloraxis_colorbar=dict(title="N° Líneas")
)
st.plotly_chart(fig, use_container_width=True)


# === High Connectivity Stops ===
st.header("Áreas de Alta Conectividad")

st.markdown("""
Debido a que las paradas no siempre están geolocalizadas de forma idéntica 
(a veces difieren algunos metros), se utiliza un **hexbin espacial** para 
identificar **áreas con alta concentración de líneas**, en lugar de puntos individuales.
""")

# Slider para resolución
gridsize = st.slider(
    "Resolución del hexbin (menor = más detalle)",
    min_value=20,
    max_value=60,
    value=35,
    step=5
)
# --- Stop–line occurrences ---
stops_lines = (
    stops[["geometry"] + line_cols]
    .melt(id_vars=["geometry"], value_vars=line_cols, value_name="line")
    .dropna(subset=["line"])
)
stops_lines["line"] = stops_lines["line"].astype(int)
# Proyectar a metros
stops_lines_m = (
    gpd.GeoDataFrame(stops_lines, geometry="geometry", crs="EPSG:4326")
    .to_crs(epsg=32721)
)
barrios_m = barrios.to_crs(epsg=32721)
x = stops_lines_m.geometry.x
y = stops_lines_m.geometry.y
minx, miny, maxx, maxy = barrios_m.total_bounds

# --- Plot ---
fig, ax = plt.subplots(figsize=(5, 5), dpi=90)
# base
barrios_m.plot(
    ax=ax,
    color="white",
    edgecolor="lightgray",
    linewidth=0.5
)
# Hexbin
hb = ax.hexbin(
    x, y,
    gridsize=gridsize,
    extent=(minx, maxx, miny, maxy),
    mincnt=1,
    cmap="viridis",
    alpha=0.85
)
# Colorbar
cbar = fig.colorbar(hb, ax=ax)
cbar.set_label("Stop–line occurrences por hexágono")

ax.set_title("Áreas servidas por muchas líneas")
ax.set_axis_off()

plt.tight_layout()
st.pyplot(fig, use_container_width=True)
