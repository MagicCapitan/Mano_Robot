#include <Servo.h>

int servoPin1 = 6;
Servo motor1;

void setup() {
  motor1.attach(servoPin1);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int values[4];
    
    // Divide la cadena en partes utilizando comas
    int index = 0;
    int startIndex = 0;
    for (int i = 0; i < 4; i++) {
      index = data.indexOf(',', startIndex);
      values[i] = data.substring(startIndex, index).toInt();
      startIndex = index + 1;
    }
    
    // Aquí puedes procesar los valores como desees
    int val1 = values[0];
    int val2 = values[1];
    int val3 = values[2];
    int val4 = values[3];

    motor1.write(val2);
    
    // Ejemplo de procesamiento: suma de los valores
   /* int sum = val1 + val2 + val3 + val4;
    Serial.println("La suma es: " + String(sum));
*/
    // Procesa los valores aquí
  }
}
