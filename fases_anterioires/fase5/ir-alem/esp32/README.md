 # Monitoramento de Plantação com ESP32 e MQTT
 
 Este projeto utiliza um microcontrolador ESP32 para coletar dados de sensores de temperatura, umidade e luminosidade, e enviá-los para um broker MQTT. Os dados são consumidos por uma aplicação em Streamlit que utiliza um algoritmo de Machine Learning para predizer a saúde de uma planta.
 
 ## Funcionalidades
 
 - **Leitura de Sensores:**
   - **Temperatura e Umidade:** Utiliza um sensor DHT22 para medições precisas do ambiente.
   - **Luminosidade:** Utiliza um LDR (Resistor Dependente de Luz) para medir a intensidade da luz.
 - **Conectividade:**
   - **Wi-Fi:** Conecta-se a uma rede Wi-Fi para ter acesso à internet.
   - **MQTT:** Publica os dados coletados em um tópico MQTT específico, permitindo que outras aplicações (como o dashboard em Streamlit) se inscrevam e recebam as informações em tempo real.
 - **Resiliência:**
   - Possui lógica para reconexão automática ao broker MQTT caso a conexão seja perdida.
 
 ## Hardware Necessário
 
 - ESP32 Dev Kit
 - Sensor de Temperatura e Umidade DHT22
 - Resistor LDR (Light Dependent Resistor)
 - Resistor de 10kΩ (para o circuito do LDR)
 - Protoboard e Jumpers para as conexões
 
 ## Circuito
 
 As conexões dos componentes ao ESP32 devem ser feitas da seguinte forma:
 
 - **Sensor DHT22:**
   - **Pino VCC:** Conectar ao pino 3.3V do ESP32.
   - **Pino GND:** Conectar ao pino GND do ESP32.
   - **Pino de Dados:** Conectar ao pino **GPIO 4 (D4)** do ESP32.
 
 - **Sensor LDR:**
   - **Um terminal do LDR:** Conectar ao pino 3.3V do ESP32.
   - **O outro terminal do LDR:** Conectar ao pino **GPIO 36 (VP)** do ESP32.
   - **Resistor de 10kΩ:** Conectar entre o pino **GPIO 36 (VP)** e o **GND**.
 
 ## Configuração e Execução
 
 Este código foi desenvolvido para ser utilizado com o [Wokwi](https://wokwi.com/), um simulador online para ESP32, Arduino e outros microcontroladores.
 
 1.  **Configuração da Rede:**
     - O código está pré-configurado para usar a rede Wi-Fi do Wokwi.
       ```cpp
       const char* ssid = "Wokwi-GUEST";
       const char* password = "";
       ```
     - Se for utilizar um ESP32 físico, altere o `ssid` e `password` para as credenciais da sua rede Wi-Fi.
 
 2.  **Configuração do MQTT:**
     - **Broker:** O broker público `broker.hivemq.com` está sendo utilizado.
     - **Tópico:** Os dados são publicados no tópico `plantacao/esp32/dados`. Certifique-se de que sua aplicação Streamlit está inscrita neste mesmo tópico para receber os dados.
 
 3.  **Bibliotecas Necessárias (PlatformIO):**
     O arquivo `platformio.ini` já deve conter as dependências necessárias. Caso precise configurar manualmente, as bibliotecas são:
     - `PubSubClient` by Nick O'Leary
     - `DHT sensor library` by Adafruit
     - `Adafruit Unified Sensor` by Adafruit
 
 4.  **Execução:**
     - Abra o projeto no Wokwi ou compile e envie para o seu ESP32 usando a IDE do Arduino ou o PlatformIO.
     - Abra o Monitor Serial com a velocidade (baud rate) de `115200` para acompanhar o status da conexão e os dados que estão sendo publicados.
 
 ## Formato do Payload
 
 A cada 2 segundos, o ESP32 envia uma mensagem para o tópico MQTT com os dados dos sensores no seguinte formato CSV:
 
 ```
 <temperatura>,<umidade>,<luminosidade>
 ```
 
 **Exemplo:** `25.50,65.30,850`
 
> Para ver a aplicação Streamlit [clique aqui](../stramlit/README.md)