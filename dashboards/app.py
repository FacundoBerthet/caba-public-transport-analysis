import streamlit as st

st.set_page_config(
    page_title="CABA - Análisis Paradas de Colectivo",
    page_icon="🚌",
    layout="wide"
)

st.title("Análisis Paradas de Colectivo - CABA")

st.markdown("""
Este proyecto explora **cómo se distribuyen las paradas de colectivo en la Ciudad Autónoma de Buenos Aires (CABA)**.
La idea es obtener una vista general, **comparar áreas** y **detectar patrones** a partir de mapas y métricas simples.

### Origen de los datos
La información original proviene de **fuentes de datos abiertos de la Ciudad de Buenos Aires** ([Portal de Datos Abiertos de la Ciudad](https://buenosaires.gob.ar/innovacionytransformaciondigital/datos-abiertos-de-buenos-aires)), en formatos GeoJSON.
Estos datos fueron **limpiados, normalizados y procesados** como parte del proyecto (se corrigieron nombres, se estandarizaron columnas y se generaron archivos listos para análisis), para obtener conjuntos de datos consistentes y listos para el análisis:
- **Paradas** (`stops`): ubicación de paradas de colectivo.
- **Calles** (`streets`): geometrías de calles normalizadas.
- **Comunas** (`comunas`): límites administrativos.
- **Barrios** (`barrios`): límites por barrio.

### Preguntas de guía:
- ¿Cuántas paradas de colectivo hay en total y cómo se distribuyen entre **comunas** y **barrios**?
- ¿Qué zonas de la ciudad concentran la **mayor cantidad de paradas**?
- ¿Qué comunas y barrios presentan la **mayor densidad de paradas** (paradas por km²)?
- ¿Qué **calles** concentran la mayor cantidad de paradas y dónde se localizan estos corredores?
- ¿Qué **líneas de colectivo** tienen más paradas y en qué comunas o barrios se observa mayor diversidad de líneas?
- ¿Dónde se encuentran las áreas de **mayor conectividad**, considerando la cantidad de líneas distintas que pasan por una misma parada?

Estas preguntas permiten analizar tanto la **distribución espacial** de las paradas como la **conectividad del sistema de transporte** dentro de la ciudad.
""")

st.info("Selecciona una página en el menú lateral para comenzar el análisis")

st.caption(
    "Fuente de datos: Portal de Datos Abiertos de la Ciudad de Buenos Aires — "
    "https://buenosaires.gob.ar/innovacionytransformaciondigital/datos-abiertos-de-buenos-aires"
)