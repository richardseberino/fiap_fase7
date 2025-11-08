# Monitoramento de Saúde de Plantação com IoT e Machine Learning

## Video do projeto funcionando
Para visualizar o video com o projeto rodando [Clique aqui](https://youtu.be/V88NFLW0Vgc)

## Visão Geral

Este projeto apresenta uma solução completa de Internet das Coisas (IoT) para o monitoramento em tempo real da saúde de uma plantação. O sistema utiliza um microcontrolador **ESP32** para coletar dados ambientais (temperatura, umidade e luminosidade), que são enviados via protocolo **MQTT** para uma aplicação web.

A aplicação, desenvolvida com **Streamlit**, funciona como um painel de controle que exibe os dados recebidos e utiliza um modelo de **Machine Learning** para classificar o ambiente como "saudável" ou "não saudável", fornecendo insights valiosos para a manutenção da plantação.

---

## Arquitetura do Projeto

O projeto é dividido em quatro componentes principais, cada um com sua própria documentação detalhada:

1.  **`dataset/` - Geração de Dados Sintéticos**
    *   **Responsabilidade:** Criar um dataset fictício e balanceado para treinar o modelo de classificação. Simula condições ambientais ideais e adversas (risco de fungos, estresse por calor).
    *   **Tecnologias:** Python, Pandas, NumPy.
    *   **[Saiba mais sobre a geração do dataset](dataset/README.md)**

2.  **`modelo/` - Treinamento do Modelo de Machine Learning**
    *   **Responsabilidade:** Utilizar o dataset sintético para treinar, avaliar e comparar diferentes algoritmos de classificação (como `RandomForest`, `SVC`, `XGBoost`). O melhor modelo é selecionado e salvo para uso em produção.
    *   **Tecnologias:** Scikit-learn, XGBoost, Joblib.
    *   **[Veja o processo de treinamento no Jupyter Notebook](modelo/modelo.ipynb)**

3.  **`esp32/` - Coleta e Envio de Dados (IoT)**
    *   **Responsabilidade:** Ler os dados dos sensores DHT22 (temperatura/umidade) e LDR (luminosidade) e publicá-los em um tópico MQTT em formato CSV. O código é projetado para ser executado em um ESP32, com simulação via Wokwi.
    *   **Tecnologias:** C++ (Arduino Framework), WiFi, PubSubClient (MQTT).
    *   **[Confira os detalhes do hardware e do código do ESP32](esp32/README.md)**

4.  **`streamlit/` - Painel de Monitoramento em Tempo Real**
    *   **Responsabilidade:** Conectar-se ao broker MQTT para receber os dados do ESP32, exibi-los em uma interface amigável e usar o modelo treinado para fazer predições em tempo real sobre a saúde do ambiente.
    *   **Tecnologias:** Streamlit, Paho-MQTT.
    *   **[Veja como executar e usar o painel de controle](streamlit/README.md)**

---

## 🚀 Como Executar a Solução Completa

Para ver o sistema em funcionamento, você precisa executar o **Painel Streamlit** e o **Simulador do ESP32** simultaneamente.

### Passo 1: Configuração do ambiente
Intale todas as dependencias necessárias para rodar a aplicação streamlit e treinamento do modelo através do arquivo `requirements.txt`. 
Recomendamos a criação de um ambiente virtual para tal.
1.  Crie um ambiente virtual
    ```bash
    python -m venv venv
    ```
2.  Ative o ambiente virtual
    ```bash
    source venv/bin/activate
    ```
3. Instale as dependencias
    ```bash
    pip install -r requirements.txt
    ```

### Passo 2: Iniciar o Painel de Monitoramento

1.  Navegue até o diretório da aplicação Streamlit.
    ```bash
    cd streamlit
    ```
2.  Instale as dependências (se ainda não o fez).
    ```bash
    pip install -r requirements.txt
    ```
3.  Execute a aplicação.
    ```bash
    streamlit run app.py
    ```
4.  No navegador, clique no botão **"Conectar"** na barra lateral para que o painel comece a ouvir as mensagens MQTT.

### Passo 3: Iniciar a Simulação do ESP32

1.  Acesse o projeto no Wokwi (ou configure um ESP32 físico).
2.  Inicie a simulação. O ESP32 se conectará ao Wi-Fi e começará a publicar os dados dos sensores no broker `broker.hivemq.com`.

### Passo 4: Observar os Resultados

Assim que o ESP32 publicar a primeira mensagem, o painel do Streamlit será atualizado automaticamente, exibindo os valores dos sensores e a classificação de saúde do ambiente ("AMBIENTE SAUDÁVEL" ou "AMBIENTE NÃO SAUDÁVEL").

---

## 📁 Estrutura de Pastas

```
.
├── dataset/
│   ├── gerar_dataset_ficticio.py
│   └── README.md
├── esp32/
│   ├── src/main.cpp
│   └── README.md
├── modelo/
│   ├── modelo_gridsearch.pkl
│   ├── modelo.ipynb
└── streamlit/
|   ├── app.py
|   └── README.md
└── requirements.txt
└── README.md
```