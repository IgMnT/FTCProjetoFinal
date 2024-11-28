#=======================================
#Bibliotecas
#=======================================

from haversine import haversine 
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime 
from PIL import Image
import plotly.express as px
import folium
from streamlit_folium import folium_static

#Inicialização do dataframe
df = pd.read_csv('../dataset/zomato.csv')
df1 = df

#=======================================
#Funções
#=======================================

def restaurantes_unicos(df1):
    restaurantes_unicos = df1.loc[:, 'Restaurant ID'].nunique()
    return restaurantes_unicos

def paises_unicos(df1):
    paises_unicos = df1.loc[:, 'Country Code'].nunique()
    return paises_unicos

def cidades_unicas(df1):
    cidades_unicas = df1.loc[:, 'City'].nunique()
    return cidades_unicas

def avaliacoes_unicas(df1):
    avaliacoes_unicas = df1.loc[:, 'Votes'].nunique()
    return avaliacoes_unicas

def tipos_culinaria_unicos(df1):
    tipos_culinaria_unicos = df1.loc[:, 'Cuisines'].nunique()
    return tipos_culinaria_unicos


#=======================================
#Barra Lateral
#=======================================

image_path = '../images.png'
image = Image.open(image_path)

st.sidebar.image(image, width=120)

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('## Filtros')

country = st.sidebar.multiselect(
    'Escolha os países que deseja visualizar os restaurantes:',
    [''],
    default=['']
)

#linhas_selecionadas = df1['Country Code'].isin(country)
#df1 = df1.loc[linhas_selecionadas, :]

#=======================================
#Layout
#=======================================

st.header('Visão Geral')

with st.container():
    st.metric('Restaurantes', restaurantes_unicos(df1))

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Países', paises_unicos(df1))
    with col2:
        st.metric('Cidades', cidades_unicas(df1))

with st.container():
    st.metric('Avaliacoes', avaliacoes_unicas(df1))

with st.container():
    st.metric('Tipos de Culinária', tipos_culinaria_unicos(df1))
    

