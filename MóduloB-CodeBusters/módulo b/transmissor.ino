#include "DHT.h"

// -------------------
// Configurações do sensor
// -------------------
#define DHTPIN 2       // Pino conectado ao DATA do sensor
#define DHTTYPE DHT11  // ou DHT22, dependendo do seu sensor

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600); 
  dht.begin();
}

void loop() {
  // Lê temperatura e umidade
  float temperatura = dht.readTemperature();
  float umidade = dht.readHumidity();

  // Verifica se houve erro na leitura
  if (isnan(temperatura) || isnan(umidade)) {
    Serial.println("Erro ao ler o sensor");
  } else {
    // Envia apenas números separados por vírgula
    Serial.print(temperatura, 2); // 2 casas decimais
    Serial.print(",");
    Serial.println(umidade, 2);
  }

  delay(5000); // Espera 5 segundos
}
