#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

#define DHT_PIN 4      // Pino digital DHT22 (D4)
#define LDR_PIN 36     // Pino analógico LDR (VP)
#define DHT_TYPE DHT22

DHT dht(DHT_PIN, DHT_TYPE);

// CONFIGURAÇÕES DA REDE PARA COMUNICAÇÃO MQTT
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// MQTT
const char* mqtt_server = "broker.hivemq.com";
const char* mqtt_topic = "plantacao/esp32/dados"; 

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi conectado!");
  Serial.println("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect_mqtt() {
  while (!client.connected()) {
    Serial.print("Tentando conexão MQTT...");
    if (client.connect("ESP32Client-Wokwi")) { // ID do cliente
      Serial.println("conectado!");
    } else {
      Serial.print("falhou, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  setup_wifi();
  client.setServer(mqtt_server, 1883); // Porta MQTT
}

void loop() {
  if (!client.connected()) {
    reconnect_mqtt();
  }
  client.loop();

  delay(2000);

  float umidade = dht.readHumidity();
  float temperatura = dht.readTemperature();
  int luz = analogRead(LDR_PIN);

  if (isnan(umidade) || isnan(temperatura)) {
    Serial.println("Falha ao ler do sensor DHT!");
    return;
  }

  String payload = String(temperatura) + "," + String(umidade) + "," + String(luz);
  
  char msg[50];
  payload.toCharArray(msg, 50);

  // Publica a mensagem no MQTT
  client.publish(mqtt_topic, msg);
  
  Serial.print("Mensagem publicada no tópico ");
  Serial.print(mqtt_topic);
  Serial.print(": ");
  Serial.println(payload);
}