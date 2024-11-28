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
df1['Preco médio'] = df1.loc[:, ['Average Cost for two', 'Country Code']].groupby('Country Code').mean()
df1.loc[:, ['Average Cost for two', 'Country Code']]