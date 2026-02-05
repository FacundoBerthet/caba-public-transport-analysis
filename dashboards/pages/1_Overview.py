import streamlit as st
import geopandas as gpd
import plotly.express as px

from utils.io import load_data
from utils.metrics import *


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

# Add stop counts
comunas = add_stop_counts(comunas, stops, "comuna")
barrios = add_stop_counts(barrios, stops, "barrio")



st.title("Overview")

st.markdown("""
En esta sección se presenta una **vista general de los conjuntos de datos** utilizados en el análisis. El objetivo es ofrecer un primer contexto antes de profundizar.
""")


# === Gral metrics ==== 
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


# === Stops by comuna ====
st.header("Paradas por Comuna")
col1, col2 = st.columns(2)

minx, miny, maxx, maxy = comunas.total_bounds
center = {"lon": (minx + maxx) / 2, "lat": (miny + maxy) / 2}

with col1:
    #bar
    fig = px.bar(
        comunas,
        x="n_stops",
        y="comuna",
        orientation="h",
        title="Número de Paradas por Comuna",
        labels={"comuna": "Comuna", "n_stops": "Número de Paradas"}
    )
    fig.update_traces(
         hovertemplate=(
            "<b>Comuna %{y}</b><br>"
            "Paradas: %{x:,}"
            "<extra></extra>"
        ),
        marker_line_color="grey",
        marker_line_width=1)
    fig.update_layout(
        yaxis=dict(type="category",categoryorder="total ascending"),
        height=600
    )
    fig.update_xaxes(showgrid=True, gridwidth=1)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    #map
    fig = px.choropleth_mapbox(
        comunas,
        geojson=comunas.__geo_interface__,
        locations=comunas.index,
        color="n_stops",
        hover_name="comuna",
        hover_data={"n_stops": True},
        mapbox_style="carto-positron",
        center=center,
        zoom=10.4,
        opacity=0.6,
        color_continuous_scale="Blues",
        title="Mapa de Paradas por Comuna"
    )
    fig.update_traces(
        hovertemplate=(
            "<b>Comuna %{hovertext}</b><br>"
            "Paradas: %{z}<extra></extra>"
        )
    )
    fig.update_layout(height=600,
                    margin={"r":0,"t":70,"l":0,"b":0},
                    coloraxis_colorbar=dict(title=None))
    st.plotly_chart(fig, use_container_width=True)


# === Stops by barrio ====
st.header("Paradas por Barrio")
col1, col2 = st.columns(2)

with col1:
    top_n = st.slider("Seleccionar Top N barrios", 5, 48, 10)

with col2:
    st.write("") 

# barh
fig = px.bar(
    barrios.sort_values(by="n_stops", ascending=False).head(top_n),
    x="n_stops",
    y="barrio",
    orientation="h",
    title=f"Top {top_n} Barrios por Número de Paradas",
    labels={"n_stops": "Número de Paradas", "barrio": "Barrio"}
)
fig.update_xaxes(showgrid=True, gridwidth=1)
fig.update_layout(height=700, yaxis={'categoryorder':'total ascending'})
fig.update_traces(
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Paradas: %{x:,}"
        "<extra></extra>"
    ),
    marker_line_color="grey",
    marker_line_width=1
)
st.plotly_chart(fig, use_container_width=True)

#map
fig = px.choropleth_mapbox(
    barrios,
    geojson=barrios.__geo_interface__,
    locations=barrios.index,
    color="n_stops",
    hover_name="barrio",
    hover_data={"n_stops": True},
    mapbox_style="carto-positron",
    center=center,
    zoom=10.6,
    opacity=0.6,
    color_continuous_scale="Blues",
    title="Mapa de Paradas por Barrio"
)
fig.update_layout(height=600, margin={"r":0,"t":30,"l":0,"b":0})
fig.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "Paradas: %{z:,}"
        "<extra></extra>"
    )
)
st.plotly_chart(fig, use_container_width=True)

# ===== stops visualization=====
st.header("Visualizacion de Paradas")
tab1, tab2 = st.tabs(["Mapa de Densidad de Paradas", "Mapa de Paradas (Filtrable)"])

with tab1:
    st.markdown("Este mapa muestra la **concentración general** de paradas en la ciudad usando un mapa de calor.")
    fig = px.density_mapbox(
    stops,
    lat=stops.geometry.y,
    lon=stops.geometry.x,
    radius=3.5,                 
    center=center,
    zoom=10.6,
    mapbox_style="carto-positron",
    color_continuous_scale="Cividis",
    opacity=0.7,
    title="Densidad de paradas de colectivo"
    )
    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        coloraxis_showscale=False
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("Este mapa muestra **cada parada individualmente** y filtrar por cantidad de lineas.")
    
    #filter
    col1, col2 = st.columns([2, 1])
    with col1:
        min_lines = st.slider(
            "Filtrar por mínimo de líneas",
            min_value=0,
            max_value=int(stops["n_lines"].max()),
            value=0,
            help="Mostrar solo paradas con al menos N líneas"
        )
    with col2:
        st.write("")
    #apply filter
    filtered_stops = stops[stops["n_lines"] >= min_lines] if min_lines > 0 else stops.copy()

    #display stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Paradas mostradas", len(filtered_stops))
    with col2:
        st.metric("% del total", f"{len(filtered_stops)/len(stops)*100:.1f}%")

    # map
    fig = px.scatter_mapbox(
    filtered_stops,
    lat=filtered_stops.geometry.y,
    lon=filtered_stops.geometry.x,
    color="n_lines",
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    center=center,
    zoom=10.6,
    opacity=0.7,
    size_max=8,
    custom_data=["direccion", "barrio", "comuna", "n_lines"])
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Barrio: %{customdata[1]}<br>"
            "Comuna: %{customdata[2]}<br>"
            "Líneas: %{customdata[3]}<extra></extra>"
    ))
    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    ) 
    fig.update_layout(
    coloraxis_colorbar=dict(
        title="Líneas"
    )) 
    st.plotly_chart(fig, use_container_width=True)