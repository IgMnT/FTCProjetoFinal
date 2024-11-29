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


def cidade_mais_restaurantes(df1):
    """Esta função retorna a cidade com maior quantidade de restaurantes
    
    Input: Dataframe
    Output: Tupla com nome da cidade e quantidade de restaurantes
    """
    # Agrupa por cidade e conta os restaurantes
    cidade_restaurantes = df1.loc[:, ['City', 'Restaurant ID']].groupby('City').count().reset_index()
    
    # Ordena em ordem decrescente e pega a primeira cidade
    cidade_mais_rest = cidade_restaurantes.sort_values('Restaurant ID', ascending=False).iloc[0]
    
    return cidade_mais_rest['City'], cidade_mais_rest['Restaurant ID']



def cidade_mais_nota_acima_4(df1):
    cidade_restaurantes = 

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

st.header('Visão Cidades')

with st.container():
    st.markdown('### Cidade com mais restaurantes')
    cidade, qtd_restaurantes = cidade_mais_restaurantes(df1)
    st.metric(label=cidade, value=qtd_restaurantes)

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('##### ')
        
    with col2:
        st.markdown('##### ')

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('##### ')
        
    with col2:
        st.markdown('##### ')

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('##### ')
        
    with col2:
        st.markdown('##### ')