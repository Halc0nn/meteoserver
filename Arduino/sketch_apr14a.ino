//описание датчиков
#include <TroykaDHT.h>
#include <TroykaLight.h>
DHT dht(4, DHT11);
TroykaLight sensorLight(A0);

void setup() {
  //инициализация датчиков
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  //запускаем датчики
  dht.read();
  sensorLight.read();
  //чтение 1 датчика - температура
  Serial.print(dht.getTemperatureC());
  Serial.print(":");
  //чтение 1 датчика - влажность
  Serial.print(dht.getHumidity());
  Serial.print(":");
  //чтение 2 датчика - свет
  Serial.print(sensorLight.getLightLux());
  Serial.print(":");
  //добавить новые датчики (чтение) сюда

  Serial.println();
  delay(2000);
}
