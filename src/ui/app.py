
import streamlit as st
from PIL import Image
import os

st.set_page_config(
    page_title="Página Inicial",
    page_icon="🤖",
    layout="wide"
)

st.title("Sistema de Monitoramento Agrícola Inteligente")
st.markdown("**Solução tecnológica para os desafios da agricultura moderna.**")

st.markdown("---")

st.header("Bem-vindo ao Painel de Controle")
st.write(
    """
    Esta aplicação integra tecnologias de Internet das Coisas (IoT), análise de dados e Inteligência Artificial 
    para oferecer uma solução completa de monitoramento e gerenciamento agrícola. Navegue pelas seções ao lado 
    para explorar as funcionalidades.
    """
)

st.info(
    "Use o menu na barra lateral à esquerda para navegar entre as diferentes páginas da aplicação.",
    icon="👈"
)


st.header("Funcionalidades Principais")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("Gerenciamento de Dados")
        st.write(
            """
            Nesta seção, você pode gerenciar todas as informações essenciais para o sistema. 
            Adicione, edite ou remova dados sobre:
            - **Culturas:** Tipos de plantações e suas áreas.
            - **Locais:** Áreas específicas de plantio.
            - **Sensores:** Dispositivos de coleta de dados.
            - **Produtos:** Insumos agrícolas.
            - **Aplicações e Coletas:** Registros de atividades.
            """
        )
        if st.button("Acessar Banco de Dados", key="db_button"):
            st.switch_page("pages/1_Banco_de_Dados.py")


with col2:
    with st.container(border=True):
        st.subheader("Gráficos e Visualizações")
        st.write(
            """
            Visualize os dados coletados pelos sensores em tempo real. Acompanhe a saúde 
            da sua lavoura com gráficos interativos que permitem:
            - Filtrar dados por tipo de cultura.
            - Analisar o comportamento de sensores específicos.
            - Comparar o desempenho de diferentes locais.
            """
        )
        if st.button("Ver Gráficos", key="charts_button"):
            st.switch_page("pages/2_Graficos.py")


with col3:
    with st.container(border=True):
        st.subheader("Detecção de Pragas")
        st.write(
            """
            Utilize nosso modelo de Inteligência Artificial para detectar pragas em suas 
            plantações. Basta enviar uma imagem da lavoura e o sistema irá:
            - Identificar a presença de lagartas e percevejos.
            - Marcar as detecções na imagem.
            - Fornecer um relatório dos itens encontrados.
            """
        )
        if st.button("Analisar Imagem", key="ia_button"):
            st.switch_page("pages/3_Detecção_de_Pragas.py")
