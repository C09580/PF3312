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
st.markdown('2. BARRAS')

#VISUALIZAR GRAFICO 1
bar_chart =  Mapa[['canton','longitud']]
bar_chart.sort_values("longitud", ascending=[False], inplace=True)
bar_chart = bar_chart.head(15)


# Graficación
df = pd.DataFrame(bar_chart)
fig = px.bar(df, x= 'canton', y = 'longitud')
st.plotly_chart(fig)

#VISUALIZAR GRAFICO 2
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
st.markdown('3. PASTEL')
fig = px.pie(bar_chart, 
            names=bar_chart.index,
            values='longitud')
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig) 

#VISUALIZAR MAPA
# Creación del mapa base
m = folium.Map(location=[9.8, -84], tiles='CartoDB positron', zoom_start=8)

folium.GeoJson(data=LimiteCantonal, name='Cantones').add_to(m)
# Control de capas
folium.LayerControl().add_to(m)

Mapa = Mapa.set_index

folium.Choropleth(
            name="Densidad Vial por Canton",
            geo_data=LimiteCantonal,
            data=Mapa,
            columns=['id', 'densidad'],
            bins=8,
            key_on='feature.properties.id',
            fill_color='Reds', 
            fill_opacity=0.5, 
            line_opacity=1,
            legend_name='Cantidad de registros de presencia',
            smooth_factor=0).add_to(m)

# Despliegue del mapa
folium_static(m)   

