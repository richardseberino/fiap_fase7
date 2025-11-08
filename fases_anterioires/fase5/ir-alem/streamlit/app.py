import pandas as pd
import streamlit as st
import numpy as np
import joblib
import paho.mqtt.client as mqtt
import time
import queue

st.set_page_config(page_title="Monitor de Plantação em Tempo Real", page_icon="🌿", layout="centered")

class StreamlitMqttClient:
    def __init__(self):
        self.client = mqtt.Client(client_id=f"streamlit-client-{int(time.time())}")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.data_queue = queue.Queue()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.subscribe("plantacao/esp32/dados")
        else:
            print(f"Falha ao conectar, código de retorno {rc}\n")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8')
        self.data_queue.put(payload)

    def connect(self, broker, port):
        self.client.connect(broker, port, 60)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def get_message(self):
        try:
            return self.data_queue.get_nowait()
        except queue.Empty:
            return None

@st.cache_resource
def get_mqtt_client():
    return StreamlitMqttClient()

mqtt_client = get_mqtt_client()

@st.cache_resource
def carregar_modelo():
    try:
        return joblib.load('../modelo/modelo_gridsearch.pkl')
    except FileNotFoundError:
        st.error("Arquivo 'modelo_gridsearch.pkl' não encontrado!")
        return None

modelo = carregar_modelo()
FEATURE_NAMES = ['temperatura', 'umidade', 'luz']

st.title("🌿 Monitor de Saúde da Plantação (Wokwi + MQTT)")
st.markdown("Esta aplicação se conecta a um broker MQTT para receber dados em tempo real da sua simulação no Wokwi.")

if 'conectado' not in st.session_state:
    st.session_state.conectado = False
if 'latest_data' not in st.session_state:
    st.session_state.latest_data = None

if modelo is None:
    st.warning("O modelo não pôde ser carregado.")
else:
    if st.sidebar.button("Conectar" if not st.session_state.conectado else "Desconectar"):
        if not st.session_state.conectado:
            mqtt_client.connect("broker.hivemq.com", 1883)
            st.session_state.conectado = True
            st.sidebar.success("Conectado!")
        else:
            mqtt_client.disconnect()
            st.session_state.conectado = False
            st.session_state.latest_data = None
        st.rerun()

    st.header("Status Atual do Ambiente")
    
    if st.session_state.conectado:
        payload = mqtt_client.get_message()
        if payload:
            try:
                st.session_state.latest_data = [float(x) for x in payload.split(',')]
            except (ValueError, IndexError):
                st.warning(f"Dado mal formatado recebido: {payload}")
        
        status_placeholder = st.empty()
        col1, col2, col3 = st.columns(3)
        temp_placeholder = col1.empty()
        umid_placeholder = col2.empty()
        luz_placeholder = col3.empty()

        if st.session_state.latest_data:
            dados = st.session_state.latest_data
            
            dados_para_previsao = pd.DataFrame([dados], columns=FEATURE_NAMES)
            
            previsao = modelo.predict(dados_para_previsao)
            confianca = np.max(modelo.predict_proba(dados_para_previsao)) * 100

            if previsao[0] == 1:
                status_placeholder.success(f"CLASSIFICAÇÃO: AMBIENTE SAUDÁVEL ✅ (Confiança: {confianca:.1f}%)", icon="🌿")
            else:
                status_placeholder.error(f"CLASSIFICAÇÃO: AMBIENTE NÃO SAUDÁVEL ❌ (Confiança: {confianca:.1f}%)", icon="⚠️")

            temp_placeholder.metric("Temperatura", f"{dados[0]:.1f} °C")
            umid_placeholder.metric("Umidade", f"{dados[1]:.1f} %")
            luz_placeholder.metric("Luminosidade", f"{int(dados[2])}")
        else:
            status_placeholder.info("Aguardando a primeira mensagem do Wokwi...")

    elif not st.session_state.conectado:
        st.info("Clique em 'Conectar' na barra lateral para iniciar o monitoramento.")
time.sleep(1)
st.rerun()