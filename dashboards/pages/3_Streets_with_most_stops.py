import streamlit as st
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.io import load_data
from utils.metrics import *


# Page config
st.set_page_config(
    page_title="Streets with Most Stops",
    page_icon="🚌",
    layout="wide"
)

# Load data
stops, calles, comunas, barrios = load_data()

# Add area in km²
comunas = add_area_km2(comunas)
barrios = add_area_km2(barrios)


st.title("Calles con Más Paradas")

st.markdown("""
En esta sección se identifican las **calles con mayor concentración de paradas**. 
Estas suelen ser avenidas largas y altamente conectadas que atraviesan grandes 
porciones de la ciudad, sirviendo como corredores principales de transporte público.
""")

# Center for maps
minx, miny, maxx, maxy = comunas.total_bounds
center = {"lon": (minx + maxx) / 2, "lat": (miny + maxy) / 2}

# === Compute stops by street ===
stops_by_street = (
    stops.groupby("calle")
    .size()
    .rename("n_stops")
    .sort_values(ascending=False)
    .reset_index()
)

# === Gral metrics ====
st.subheader("Indicadores generales")
total_streets = stops["calle"].nunique()
avg_stops_per_street = stops.groupby("calle").size().mean()

col1, col2, col3, col4 = st.columns([1,1,1,1])
with col1:
    st.metric("Promedio paradas/calle", f"{avg_stops_per_street:.1f}")
with col2:
    st.metric("Calle con más paradas", stops_by_street.iloc[0]["calle"])
with col3:
    st.metric("Máximo de paradas", int(stops_by_street.iloc[0]["n_stops"]))
with col4:
    st.write("")


# === Top Streets Bar Chart ===
st.header("Ranking de Calles")

col1, col2 = st.columns(2)

with col1:
    top_n = st.slider("Seleccionar Top N calles", 5, 25, 10, key="streets_slider")

with col2:
    st.write("")

fig = px.bar(
    stops_by_street.head(top_n),
    x="n_stops",
    y="calle",
    orientation="h",
    title=f"Top {top_n} Calles por Número de Paradas",
    labels={"n_stops": "Número de Paradas", "calle": "Calle"}
)
fig.update_traces(
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Paradas: %{x:,}"
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




# === Map of Top Streets ===
st.header("Mapa de Principales Corredores")

col1, col2 = st.columns(2)

with col1:
    top_n_map = st.slider("Top N calles en el mapa", 5, 20, 10, key="map_slider")

with col2:
    st.write("") 

# Filter top N streets for map
top_streets = stops_by_street.head(top_n_map).copy()

# Join with streets geodataframe
calles_top = calles.merge(top_streets, on="calle", how="inner").copy()

st.markdown(f"""
Este mapa muestra las **{top_n_map} calles principales** con mayor número de paradas, 
destacando los principales corredores de transporte público de la ciudad.
""")

calles_top_hover = calles_top.rename(columns={
    "calle": "Calle",
    "n_stops": "Paradas"
})

m = calles_top_hover.explore(
    color="red",
    style_kwds={"weight": 3},
    tiles="CartoDB positron",
    tooltip=["Calle", "Paradas"]
)

st.components.v1.html(m._repr_html_(), height=600)


