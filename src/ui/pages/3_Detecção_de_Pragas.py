
import streamlit as st
from PIL import Image
import requests
import io
import base64
import os
import yaml

def load_config():
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        '../config',
        'api.yml'
    )
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            env = os.getenv('ENV', 'development')
            return config[env]
    return None

st.set_page_config(layout="wide", page_title="Detecção de Pragas")

st.title("Detecção de Pragas em Lavouras")
st.write("Envie uma imagem para análise. O modelo irá detectar e identificar lagartas e percevejos.")

# --- Uploader ---
uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])

config = load_config()
api_url = config.get("url_api_yolo") if config else "http://127.0.0.1:5000/predict"
api_alerta_aws = config.get("url_api_aws") if config else ""

if uploaded_file is not None:
    image_bytes = uploaded_file.getvalue()
    image = Image.open(io.BytesIO(image_bytes))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Imagem Original")
        st.image(image, caption="Imagem enviada.", use_column_width=True)

    with col2:
        st.subheader("Resultado da Análise")
        
        with st.spinner("Analisando a imagem..."):
            api_url = "http://127.0.0.1:5000/predict"
            
            try:
                files = {"file": (uploaded_file.name, image_bytes, uploaded_file.type)}
                
                response = requests.post(api_url, files=files)
                response.raise_for_status()

                result = response.json()
                
                processed_image_b64 = result.get("image")
                detections = result.get("detections", [])

                if processed_image_b64:
                    processed_image_bytes = base64.b64decode(processed_image_b64)
                    processed_image = Image.open(io.BytesIO(processed_image_bytes))
                    
                    st.image(processed_image, caption="Imagem processada com detecções.", use_column_width=True)
                else:
                    st.error("A API não retornou uma imagem processada.")

                if detections:
                    alerta_aws = "sem alertas"
                    st.write("Itens detectados:")
                    for detection in detections:
                        st.markdown(f"- **{detection}**")
                        alertas_aws = detection
                    response = requests.post(api_alerta_aws, json={"mensagem": alertas_aws})
                else:
                    st.warning("Nenhuma praga foi detectada na imagem com o limiar de confiança definido.")

            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao conectar com a API de análise: {e}")
                st.info("Verifique se o serviço da API (fases_anterioires/fase6/app/app.py) está em execução.")

else:
    st.info("Aguardando o envio de uma imagem.")
