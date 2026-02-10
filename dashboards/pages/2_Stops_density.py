import streamlit as st
import geopandas as gpd
import plotly.express as px

from utils.io import load_data
from utils.metrics import *


# Page config
st.set_page_config(
    page_title="Stops Density",
    page_icon="🚌",
    layout="wide"
)

# Load data
stops, calles, comunas, barrios = load_data()

# Add area in km²
comunas = add_area_km2(comunas)
barrios = add_area_km2(barrios)

# Add stop counts
comunas = add_stop_counts(comunas, stops, "comuna")
barrios = add_stop_counts(barrios, stops, "barrio")

# Add density
comunas = add_density(comunas)
barrios = add_density(barrios)


st.title("Densidad de Paradas")

st.markdown("""
En esta sección se analiza la **densidad de paradas por km²** en lugar de conteos absolutos.
Esto permite comparar áreas de distinto tamaño de forma equitativa, ya que comunas y barrios 
varían significativamente en superficie.
""")

# Center for maps
minx, miny, maxx, maxy = comunas.total_bounds
center = {"lon": (minx + maxx) / 2, "lat": (miny + maxy) / 2}

# === Gral metrics ====
st.subheader("Indicadores generales")

total_stops = stops.shape[0]
total_area = comunas["area_km2"].sum()
density_caba = total_stops / total_area

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Densidad CABA", f"{density_caba:.1f} paradas/km²")
with col2:
    st.metric("Área total", f"{total_area:.1f} km²")
with col3:
    st.metric("Densidad mediana (comunas)", f"{comunas['stops_per_km2'].median():.1f} paradas/km²")
with col4:
    st.metric("Densidad mediana (barrios)", f"{barrios['stops_per_km2'].median():.1f} paradas/km²")


# === Density by Comuna ====
st.header("Densidad por Comuna")
col1, col2 = st.columns(2)

with col1:
    # bar chart
    fig = px.bar(
        comunas,
        x="stops_per_km2",
        y="comuna",
        orientation="h",
        title="Densidad de Paradas por Comuna (paradas/km²)",
        labels={"comuna": "Comuna", "stops_per_km2": "Paradas por km²"}
    )
    fig.update_traces(
        hovertemplate=(
            "<b>Comuna %{y}</b><br>"
            "Densidad: %{x:.1f} paradas/km²<br>"
            "<extra></extra>"
        ),
        marker_line_color="grey",
        marker_line_width=1
    )
    fig.update_layout(
        yaxis=dict(type="category", categoryorder="total ascending"),
        height=600
    )
    fig.update_xaxes(showgrid=True, gridwidth=1)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Map
    fig = px.choropleth_mapbox(
        comunas,
        geojson=comunas.__geo_interface__,
        locations=comunas.index,
        color="stops_per_km2",
        hover_name="comuna",
        hover_data={
            "stops_per_km2": ":.1f",
            "n_stops": True,
            "area_km2": ":.2f"
        },
        mapbox_style="carto-positron",
        center=center,
        zoom=10.4,
        opacity=0.6,
        color_continuous_scale="Reds",
        title="Mapa de Densidad por Comuna"
    )
    fig.update_traces(
        hovertemplate=(
            "<b>Comuna %{hovertext}</b><br>"
            "Densidad: %{z:.1f} paradas/km²<br>"
            "Paradas: %{customdata[1]}<br>"
            "Área: %{customdata[2]:.2f} km²"
            "<extra></extra>"
        )
    )
    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 70, "l": 0, "b": 0},
        coloraxis_colorbar=dict(title="Paradas/km²")
    )
    st.plotly_chart(fig, use_container_width=True)



# === Density by Barrio ====
st.header("Densidad por Barrio")
col1, col2 = st.columns(2)

with col1:
    top_n = st.slider("Seleccionar Top N barrios", 5, 48, 15, key="density_slider")

with col2:
    st.write("")  # Spacer

# Bar chart
fig = px.bar(
    barrios.sort_values("stops_per_km2", ascending=False).head(top_n),
    x="stops_per_km2",
    y="barrio",
    orientation="h",
    title=f"Top {top_n} Barrios por Densidad (paradas/km²)",
    labels={"stops_per_km2": "Paradas por km²", "barrio": "Barrio"}
)
fig.update_traces(
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Densidad: %{x:.1f} paradas/km²"
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

# Map
fig = px.choropleth_mapbox(
    barrios,
    geojson=barrios.__geo_interface__,
    locations=barrios.index,
    color="stops_per_km2",
    hover_name="barrio",
    hover_data={
        "stops_per_km2": ":.1f",
        "n_stops": True,
        "area_km2": ":.2f"
    },
    mapbox_style="carto-positron",
    center=center,
    zoom=10.6,
    opacity=0.6,
    color_continuous_scale="Reds",
    title="Mapa de Densidad por Barrio"
)
fig.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "Densidad: %{z:.1f} paradas/km²<br>"
        "Paradas: %{customdata[1]}<br>"
        "Área: %{customdata[2]:.2f} km²"
        "<extra></extra>"
    )
)
fig.update_layout(
    height=600,
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    coloraxis_colorbar=dict(title="Paradas/km²")
)
st.plotly_chart(fig, use_container_width=True)


# === Distribution by Barrio ===
st.subheader("Distribución de Densidad entre Barrios")

fig = px.histogram(
    barrios,
    x="stops_per_km2",
    nbins=18,
    title="Distribución de densidad de paradas (barrios)",
    labels={"stops_per_km2": "Paradas por km²"}
)
fig.add_vline(
    x=barrios["stops_per_km2"].median(),
    line_dash="dash",
    line_color="black",
    annotation_text=f"Mediana: {barrios['stops_per_km2'].median():.1f}",
    annotation_position="top right"
)
fig.update_traces(marker_line_color="grey", marker_line_width=1)
fig.update_layout(height=600, showlegend=False)
fig.update_xaxes(showgrid=True, gridwidth=1)
fig.update_yaxes(showgrid=True, gridwidth=1, title_text="Cantidad de Barrios")
st.plotly_chart(fig, use_container_width=True)