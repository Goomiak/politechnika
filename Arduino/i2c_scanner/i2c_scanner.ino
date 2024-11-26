#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(9600);
  Serial.println("Szukam adresu I2C...");
  for (byte i = 8; i < 120; i++) {
    Wire.beginTransmission(i);
    if (Wire.endTransmission() == 0) {
      Serial.print("Znaleziono urządzenie na adresie: 0x");
      Serial.println(i, HEX);
    }
  }
  Serial.println("Skanowanie zakończone.");
}

void loop() {}