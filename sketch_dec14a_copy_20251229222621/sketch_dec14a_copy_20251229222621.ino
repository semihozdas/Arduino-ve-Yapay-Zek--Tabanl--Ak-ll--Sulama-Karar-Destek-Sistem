// ================== LED PINLER ==================
#define GREEN_LED 10   // Sulama VAR
#define RED_LED   9    // Sulama YOK

// ================== SENSOR PINLER ==================
#define SOIL_PIN  A0
#define LIGHT_PIN A1

void setup() {
  Serial.begin(9600);

  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);

  digitalWrite(GREEN_LED, LOW);
  digitalWrite(RED_LED, LOW);
}

void loop() {
  int soil  = analogRead(SOIL_PIN);
  int light = analogRead(LIGHT_PIN);

  // Python'a SADECE 2 değer gönder
  // FORMAT: soil,light
  Serial.print(soil);
  Serial.print(",");
  Serial.println(light);

  // Python'dan karar al
  if (Serial.available() > 0) {
    char decision = Serial.read();

    if (decision == '1') {
      digitalWrite(GREEN_LED, HIGH);
      digitalWrite(RED_LED, LOW);
    } 
    else if (decision == '0') {
      digitalWrite(GREEN_LED, LOW);
      digitalWrite(RED_LED, HIGH);
    }
  }

  delay(500);  // hızlı kontrol
}
