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
import streamlit as st
from streamlit_folium import folium_static
import plotly.express as px

#
# Configuración de la página
#
#st.set_page_config(layout='wide')


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

LimiteCantonal = gpd.read_file("https://raw.githubusercontent.com/C09580/PF3311/bf386e12cf0ee05c81ccb63599429c5f7fce07ce/limite_cantonal.geojson")
RedVial = gpd.read_file("https://raw.githubusercontent.com/C09580/PF3311/d681b7d6683d95522150f0b44ff904912c7f5425/red_vial.geojson")
Mapa = gpd.read_file("https://raw.githubusercontent.com/C09580/PF3311/d681b7d6683d95522150f0b44ff904912c7f5425/lmc-rvc.geojson")

#Agregar el canton segun la ruta utilizando geopandas
join_tabla = RedVial.sjoin(Mapa, how="left", op="intersects")
tabla = join_tabla[['canton','categoria_left','longitud_left','longitud_right','densidad']].groupby(['canton','categoria_left','longitud_right','densidad'])['longitud_left'].sum().reset_index()
tabla['longitud_left'] = tabla['longitud_left']/1000

#VISUALIZAR TABLA 1
st.markdown('1. TABLA')
tabla.sort_values("longitud_right", ascending=[False], inplace=True)

st.dataframe(tabla)


#VISUALIZAR GRAFICO 1
chart_1 = tabla.pivot(index='canton', columns='categoria_left', values='longitud_left')
chart_1 = chart_1.fillna(0)
tabla_tmp = tabla[['canton','longitud_right']].groupby(['canton'])['longitud_right'].mean()
chart_1 = chart_1.join(tabla_tmp, on='canton', rsuffix='_b',how="left")
chart_1.sort_values("longitud_right", ascending=[False], inplace=True)
chart_3 = chart_1.copy()
chart_1 = chart_1.head(15)
chart_1['cantones'] = chart_1.index
st.markdown('2. GRAFICO BARRAS')

# Graficación
fig = px.bar(chart_1[['cantones','longitud_right']], 
labels={'cantones':'Canton', 'longitud_right':'Longitud vial'})
st.plotly_chart(fig)





