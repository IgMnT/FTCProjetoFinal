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
    comparison_dfx = df1.groupby('has_online_delivery')['votes'].mean().reset_index()
    comparison_dfx.columns = ['Delivery Online', 'Média de Avaliações']
    
    comparison_dfx['Delivery Online'] = comparison_dfx['Delivery Online'].map({
        1: 'Com Pedido Online',
        0: 'Sem Pedido Online'
    })
    
    return comparison_dfx

def restaurante_reserva_valor_medio(df1):
    # Restaurantes com reserva
    df_com_reserva = df1[df1['has_table_booking'] == 1]
    avg_price_com_reserva = df_com_reserva['average_cost_for_two'].mean()
    
    # Restaurantes sem reserva
    df_sem_reserva = df1[df1['has_table_booking'] == 0]
    avg_price_sem_reserva = df_sem_reserva['average_cost_for_two'].mean()
    
    # Criando DataFrame com os resultados
    comparison_df = pd.DataFrame({
        'Reserva': ['Com Reserva', 'Sem Reserva'],
        'Média de Preço para duas pessoas': [avg_price_com_reserva, avg_price_sem_reserva]
    })
    
    return comparison_df

def restaurante_culinaria_japonesa_bbq(df1):
    culinaria_japonesa = df1[
        (df1['cuisines'] == 'Japanese') & 
        (df1['country_code'] == 216)
    ][['cuisines', 'average_cost_for_two']].copy()
    
    BBQ = df1[
        (df1['cuisines'] == 'BBQ') & 
        (df1['country_code'] == 216)
    ][['cuisines', 'average_cost_for_two']].copy()
    
    culinaria_japonesa_media = culinaria_japonesa.groupby('cuisines')['average_cost_for_two'].mean().reset_index()
    BBQ_media = BBQ.groupby('cuisines')['average_cost_for_two'].mean().reset_index()
    media_total = pd.concat([culinaria_japonesa_media, BBQ_media]).reset_index(drop=True)
    
    return media_total

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
        comparison_dfx = restaurante_pedido_online_avaliacoes_medias(df1)
        st.dataframe(comparison_dfx)
    with col2:
        st.markdown('#### Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?')
        comparison_df = restaurante_reserva_valor_medio(df1)
        st.dataframe(comparison_df)
with st.container():
    st.markdown('#### Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?')
    media_total = restaurante_culinaria_japonesa_bbq(df1)
    st.dataframe(media_total)
