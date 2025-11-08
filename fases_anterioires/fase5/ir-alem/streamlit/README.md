# Streamlit

## 📝 Visão Geral

Este projeto consiste em uma aplicação web desenvolvida com **Streamlit** que funciona como um painel de monitoramento em tempo real para a saúde de uma plantação.

A aplicação recebe dados de sensores (temperatura, umidade e luminosidade) via protocolo **MQTT**, processa esses dados com um modelo de **Machine Learning** para classificar o ambiente como "saudável" ou "não saudável" e exibe o status atual em uma interface amigável.

## ✨ Funcionalidades

O script `app.py` é o coração da aplicação e possui as seguintes responsabilidades:

1.  **Interface Web (UI):**
    *   Cria um painel de controle interativo usando a biblioteca `streamlit`.
    *   Exibe o status da conexão MQTT e as leituras atuais dos sensores (Temperatura, Umidade, Luminosidade).
    *   Apresenta a classificação do ambiente ("AMBIENTE SAUDÁVEL" ou "AMBIENTE NÃO SAUDÁVEL") com base na predição do modelo, incluindo um percentual de confiança.

2.  **Comunicação MQTT:**
    *   Gerencia a conexão com um broker MQTT público (`broker.hivemq.com`).
    *   Se inscreve no tópico `plantacao/esp32/dados` para receber as mensagens enviadas pelo dispositivo (ESP32).
    *   Processa as mensagens recebidas de forma assíncrona para não bloquear a interface.

3.  **Inteligência Artificial (Machine Learning):**
    *   Carrega um modelo de classificação pré-treinado (`modelo_gridsearch.pkl`).
    *   Utiliza os dados dos sensores para fazer uma predição em tempo real sobre a saúde da plantação.

4.  **Gerenciamento de Estado e Atualização em Tempo Real:**
    *   Usa o `st.session_state` para manter o estado da aplicação.
    *   A página é atualizada a cada segundo para buscar novas mensagens e atualizar a interface, criando um efeito de tempo real.

---

## 🚀 Como Executar a Aplicação

Para rodar este projeto, você precisará ter o Python instalado e seguir os passos abaixo.

### 1. Pré-requisitos

*   Python 3.8+
*   Pip (gerenciador de pacotes do Python)

### 2. Estrutura de Pastas

Certifique-se de que sua estrutura de pastas esteja organizada conforme o esperado pelo script. O arquivo do modelo de Machine Learning deve estar em um diretório `modelo` no nível acima do diretório `stramlit`.

```
.
├── modelo/
│   └── modelo_gridsearch.pkl
└── stramlit/
    └── app.py
```

### 3. Instalação de Dependências

Abra seu terminal, navegue até a pasta do projeto e instale as dependências com o pip:

```bash
pip install -r requirements.txt
```

### 4. Executando o Servidor Streamlit

Com as dependências instaladas, você pode iniciar a aplicação.

1.  Abra o terminal.
2.  Navegue até o diretório onde o arquivo `app.py` está localizado. Por exemplo:
    ```bash
    cd "stramlit"
    ```
3.  Execute o seguinte comando:
    ```bash
    streamlit run app.py
    ```

Seu navegador padrão deverá abrir automaticamente com a aplicação em execução.

### 5. Utilização

1.  Com a página da aplicação aberta, clique no botão **"Conectar"** na barra lateral. A aplicação se conectará ao broker MQTT.
2.  Inicie sua simulação no Wokwi (ou qualquer outro cliente MQTT) para que ela comece a publicar os dados dos sensores no tópico `plantacao/esp32/dados` no broker `broker.hivemq.com`.
3.  Assim que a primeira mensagem for recebida, o painel será atualizado com os valores de temperatura, umidade, luminosidade e a classificação de saúde do ambiente.

---

## 🤖 Sobre o Modelo

O modelo de Machine Learning (`modelo_gridsearch.pkl`) foi treinado para classificar o estado da plantação com base nos dados dos sensores. Ele é carregado no início da aplicação e usado para fazer inferências em tempo real.

As features esperadas pelo modelo são: `temperatura`, `umidade` e `luz`.

Para saber mais sobre o processo de treinamento do modelo [clique aqui](../modelo/modelo_gridsearch.ipynb)