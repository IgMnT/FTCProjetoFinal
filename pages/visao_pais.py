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

df1['Price range'] = df1['Price range'].astype(int)
df1['Country Code'] = df1['Country Code'].astype(int)
df1['Votes'] = df1['Votes'].astype(int)
df1.loc[df1['Has Table booking'] == 1, 'Has Table booking'] = True
df1.loc[df1['Has Table booking'] == 0, 'Has Table booking'] = False

#=======================================
#Funções
#=======================================





COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]




def pais_top(df1,col):
    linha = df.loc[df[col].idxmax()]
    pais_code = linha['Country Code']
    pais = country_name(pais_code)
    return pais

def nivel_preco(df1):
    code = df1.loc[df1['Price range'] == 4, 'Country Code'].value_counts().idxmax()
    pais = country_name(code)
    return pais

def cuisines(df1):
    culinarias_distintas = df.groupby('Country Code')['Cuisines'].nunique()
    pais_mais_diverso = culinarias_distintas.idxmax()
    pais = country_name(pais_mais_diverso)
    return pais

def entregas_reservas(df1,col):
    code = df1.loc[df1[col] == True, 'Country Code'].value_counts().idxmax()
    pais = country_name(code)
    return pais
  
def media_avaliacoes(df1, col, func):
    media = df1.groupby('Country Code')[col].mean()
    country_id = media.idxmax() if func == pd.Series.idxmax else media.idxmin()
    return country_name(country_id)

def prato_pais(df1):
    preco_medio = df1.groupby('Country Code')['Average Cost for two'].mean()
    visao = preco_medio.reset_index(name='Preco médio')
    visao['Country Code'] = visao['Country Code'].apply(country_name)
    visao = visao.rename(columns={'Country Code': 'País'})
    return visao





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

st.header('Visão País')

with st.container():
    col1,col2 = st.columns(2)
    
    with col1:
        st.markdown('### País com maior quantidade de cidades registradas')
        col = 'City'
        pais = pais_top(df1,col)
        st.subheader(pais)
    with col2:
        st.markdown('### País com maior quantidade de restaurantes cadastrados')
        col = 'Restaurant ID'
        pais = pais_top(df1,col)
        st.subheader(pais)

with st.container():
    st.markdown('### país que possui mais restaurantes com o nível de preço igual a 4 registrados')
    pais = nivel_preco(df1)
    st.subheader(pais)

with st.container():
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('### País com maior quantidade de culinarias distintas')
        col = 'Cuisines'
        pais = cuisines(df1)
        st.subheader(pais)
    with col2:
        st.markdown('### País com maior quantidade de avaliações registradas')
        col = 'Votes'
        pais = pais_top(df1,col)
        st.subheader(pais)

with st.container():
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('### País com maior quantidade de restaurantes com entregas')
        col = 'Has Online delivery'
        pais = entregas_reservas(df1,col)
        st.subheader(pais)
    with col2:
        st.markdown('### País com maior quantidade de restaurantes com reservas')
        col = 'Has Table booking'
        pais = entregas_reservas(df1,col)
        st.subheader(pais)
with st.container():
    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown('### País com maior quantidade média de avaliações:')
        col = 'Votes'
        pais = media_avaliacoes(df1,col,pd.Series.idxmax)
        st.subheader(pais)
    with col2:
        st.markdown('### País com maior média de nota:')
        col = 'Aggregate rating'
        pais = media_avaliacoes(df1,col,pd.Series.idxmax)
        st.subheader(pais)
    with col3:
        st.markdown('### País com menor média de nota:')   
        col = 'Aggregate rating'
        pais = media_avaliacoes(df1,col,pd.Series.idxmin)
        st.subheader(pais)
with st.container():
    st.markdown('### Média de preço de prato para dois p/ país:')
    visao = prato_pais(df1)
    st.dataframe(visao)


    

   



    
    


