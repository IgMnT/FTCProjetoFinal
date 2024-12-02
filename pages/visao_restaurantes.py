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
import inflection

#=======================================
#Funções
#=======================================

def rename_columns(df):
    df = df.copy()
    
    # Renomeando colunas
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    
    df['restaurant_id'] = df['restaurant_id'].fillna(0).astype(int)
    df['country_code'] = df['country_code'].fillna(0).astype(int)
    
     
    text_columns = ['restaurant_name', 'city', 'address', 'locality', 
                   'locality_verbose', 'currency', 'rating_color', 'rating_text']
    for col in text_columns:
        df[col] = df[col].fillna('').astype(str)
    
    df['longitude'] = df['longitude'].fillna(0.0).astype(float)
    df['latitude'] = df['latitude'].fillna(0.0).astype(float)
    
    df['cuisines'] = df['cuisines'].fillna('').astype(str)
    df['cuisines'] = df['cuisines'].apply(lambda x: x.split(',')[0] if x != '' else x)
    
    df['average_cost_for_two'] = df['average_cost_for_two'].fillna(0).astype(float)
    df['aggregate_rating'] = df['aggregate_rating'].fillna(0.0).astype(float)
    
    bool_columns = ['has_table_booking', 'has_online_delivery', 
                   'is_delivering_now', 'price_range', 'votes']
    for col in bool_columns:
        df[col] = df[col].fillna(0).astype(int)
    
    return df

df = pd.read_csv('../dataset/zomato.csv')
df1 = rename_columns(df)


def restaurante_mais_avaliado(df1):
    idx = df1['votes'].idxmax()
    restaurante = df1.loc[idx, 'restaurant_name']
    votos_restaurante = df1.loc[idx, 'votes']
    return restaurante, votos_restaurante

def restaurante_maior_nota(df1):
    idx = df1['aggregate_rating'].idxmax()
    restaurante = df1.loc[idx, 'restaurant_name']
    nota = df1.loc[idx, 'aggregate_rating']
    return restaurante, nota

def restaurante_mais_caro(df1):
    idx = df1['average_cost_for_two'].idxmax()
    restaurante = df1.loc[idx, 'restaurant_name']
    preco = df1.loc[idx, 'average_cost_for_two']
    preco_prefixo = df1.loc[idx,'currency'].split('(')[1].split(')')[0]
    return restaurante, preco, preco_prefixo

def restaurante_menor_nota_brazil(df1):
    idx = (df1[df1['cuisines'] == 'Brazilian']['aggregate_rating'].idxmin())
    restaurante = df1.loc[idx, 'restaurant_name']
    nota = df1.loc[idx, 'aggregate_rating']
    return restaurante, nota

def restaurante_brasileiro_maior_nota_brazil(df1):
    mask = (df1['cuisines'] == 'Brazilian') & (df1['country_code'] == 30)
    idx = df1.loc[mask, 'aggregate_rating'].idxmax()
    restaurante = df1.loc[idx, 'restaurant_name']
    nota = df1.loc[idx, 'aggregate_rating']
    return restaurante, nota

def restaurante_pedido_online_avaliacoes_medias(df1):
    # Agrupa por has_online_delivery e calcula as médias
    comparison_df = df1.groupby('has_online_delivery').agg({
        'votes': 'mean',
        'aggregate_rating': 'mean',
        'average_cost_for_two': 'mean'
    }).reset_index()
    
    # Renomeia as colunas
    comparison_df.columns = ['Delivery Online', 'Média de Avaliações', 'Nota Média', 'Preço Médio para Dois']
    
    # Substitui os valores booleanos por descrições
    comparison_df['Delivery Online'] = comparison_df['Delivery Online'].map({
        1: 'Com Pedido Online',
        0: 'Sem Pedido Online'
    })
    
    return comparison_df


def restaurante_reserva_valor_medio(df1):
    # Calcula médias para restaurantes com pedido online
    df_delivery = df1[df1['has_online_delivery'] == 1]
    avg_votes_online = df_online.groupby('aggregate_rating')['votes'].mean().reset_index()
    avg_votes_online = avg_votes_online.sort_values('votes', ascending=False).head(5)
    avg_votes_online.columns = ['Nota', 'Média de Avaliações']
    avg_votes_online['Tipo'] = 'Com Pedido Online'
    
    # Calcula médias para restaurantes sem pedido online
    df_offline = df1[df1['has_online_delivery'] == 0]
    avg_votes_offline = df_offline.groupby('aggregate_rating')['votes'].mean().reset_index()
    avg_votes_offline = avg_votes_offline.sort_values('votes', ascending=False).head(5)
    avg_votes_offline.columns = ['Nota', 'Média de Avaliações']
    avg_votes_offline['Tipo'] = 'Sem Pedido Online'
    
    # Combina os dois dataframes
    comparison_df = pd.concat([avg_votes_online, avg_votes_offline])
    return comparison_df



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

#linhas_selecionadas = df1['country_code'].isin(country)
#df1 = df1.loc[linhas_selecionadas, :]



#=======================================
#Layout
#=======================================

st.header('Visão Restaurantes')

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('#### Restaurante mais avaliado')
        restaurante, votos_restaurante = restaurante_mais_avaliado(df1)
        st.metric(label=restaurante, value=f'{votos_restaurante} votos')
    with col2:
        st.markdown('#### Restaurante com maior nota')
        restaurante, nota = restaurante_maior_nota(df1)
        st.metric(label = restaurante, value=f'{nota} estrelas')
with st.container():
    st.markdown('#### Restaurante mais caro')
    restaurante, preco, preco_prefixo = restaurante_mais_caro(df1)
    st.metric(label = restaurante, value=f'{preco_prefixo}{preco}')

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('#### Restaurante de culinaria brasileira com menor nota')
        restaurante, nota = restaurante_menor_nota_brazil(df1)
        st.metric(label = restaurante, value=f'{nota} estrelas')
    
    with col2:
        st.markdown('#### Restaurante brasileiro de culinaria brasileira com maior nota')
        restaurante, nota = restaurante_brasileiro_maior_nota_brazil(df1)
        st.metric(label = restaurante, value=f'{nota} estrelas')

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('#### Os restaurantes que aceitam pedido online são também, na média, osrestaurantes que mais possuem avaliações registradas?')
        comparison_df = restaurante_pedido_online_avaliacoes_medias(df1)
        st.dataframe(comparison_df)
    with col2:
        st.markdown('#### ')

with st.container():
    st.markdown('#### ')