# Pryecto PF3312-Desarrollo de tablero de datos en Streamlit


import math
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import folium
from folium import Marker
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
import requests
from geojson import dump
import fiona
import fiona.crs
from shapely.geometry import Point, mapping, shape
from owslib.wfs import WebFeatureService


#
# Configuración de la página
#
st.set_page_config(layout='wide')


#
# TÍTULO Y DESCRIPCIÓN DE LA APLICACIÓN
#

st.title('Visualización Densidad Vial por Canton')
st.markdown('Esta aplicación presenta visualizaciones tabulares, gráficas y geoespaciales de datos de limites cantonales, red vial y densidad de carreteras por cantón')


#
# ENTRADAS
#

# Carga de datos
# Carga de registros de presencia de murciélagos en un dataframe de pandas

LimiteCantonal = gpd.read_file("https://github.com/C09580/PF3311/blob/bf386e12cf0ee05c81ccb63599429c5f7fce07ce/limite_cantonal.geojson")
RedVial = gpd.read_file("https://github.com/C09580/PF3311/blob/d681b7d6683d95522150f0b44ff904912c7f5425/red_vial.geojson")
Mapa = gpd.read_file("https://github.com/C09580/PF3311/blob/d681b7d6683d95522150f0b44ff904912c7f5425/lmc-rvc.geojson")

#Agregar el canton segun la ruta utilizando geopandas
join_tabla = RedVial.sjoin(Mapa, how="left", op="intersects")
tabla = join_tabla[['canton','categoria_left','longitud_left','longitud_right','densidad']].groupby(['canton','categoria_left','longitud_right','densidad'])['longitud_left'].sum().reset_index()
tabla['longitud_left'] = tabla['longitud_left']/1000

#VISUALIZAR TABLA 1
st.markdown('1. TABLA')
tabla.sort_values("longitud_right", ascending=[False], inplace=True)

st.dataframe(tabla)





