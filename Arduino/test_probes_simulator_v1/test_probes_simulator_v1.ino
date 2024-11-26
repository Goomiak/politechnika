#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define Servo_PWM 9
Servo MG995_Servo;  


LiquidCrystal_I2C lcd(0x3F, 20, 4); 


long liczba_cykli = 10000; 
int czas_h = 1;
int czas_min = 40;

void setup() {
  Serial.begin(9600);
  MG995_Servo.attach(Servo_PWM);  
  
  
  lcd.init();  
  lcd.backlight();


  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Symulacja pracy");
  lcd.setCursor(0, 1);
  lcd.print("elektrod testowych");
  lcd.setCursor(0, 2);
  lcd.print("autor K. Jankowski");
  lcd.setCursor(0, 3);
  lcd.print("Program v.1.0.0");
  
  delay(10000);  
  

  for (int i = 10; i >= 0; i--) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Start testu za ");
    lcd.print(i);
    lcd.print(" s");
    delay(1000);  
  }
  
  lcd.clear();
}

void loop() {
  if (liczba_cykli > 0) {
    
    lcd.setCursor(0, 0);
    lcd.print("Liczba cykli - ");
    lcd.setCursor(13, 0);  
    lcd.print("      ");    
    lcd.setCursor(13, 0);   
    lcd.print(liczba_cykli);  

    lcd.setCursor(0, 1);
    lcd.print("Czas - ");
    lcd.print(czas_h);
    lcd.print("h ");
    lcd.print(czas_min);
    lcd.print("m");

    MG995_Servo.write(165);  
    delay(300);
    MG995_Servo.write(175); 
    delay(300);
    

    liczba_cykli--;  
    if (liczba_cykli % 100 == 0) {
      czas_min--;  
      if (czas_min < 0) {
        czas_h--;
        czas_min = 59;
      }
    }
  } else {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Test zakonczony");
    while (1);  
  }
}
