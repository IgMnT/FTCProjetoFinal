import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon='🏠',
)


image_path = './images.png'
image = Image.open( image_path )
st.sidebar.image (image, width=120)
st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('## Dados para a Fome Zero')
st.sidebar.markdown("""___""")
st.write("# Fome Zero Dashboard")
st.markdown(
    """
    ### 📈 Fome Zero Dashboard
    ### Como usar:
    - Visão Geral
    - Visão Cidade
    - Visão Restaurantes
    - Visão País
    - Visão Culinaria
    
    """
)