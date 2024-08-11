#include<Servo.h>

int servoPin1 = 6;
int servoPos1 = 0;//el angulo del servo motor
Servo motor1;//Nombre del servo motor

void setup() {
  motor1.attach(servoPin1);
  Serial.begin(9600); // Inicializar la comunicación serial a 9600 baudios
  delay(5000); // Esperar 5 segundos para permitir abrir el monitor serie
  
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n'); // Leer datos hasta el carácter de nueva línea
    int numero = data.toInt(); // Convertir la cadena de texto en un entero
    Serial.print("Datos recibidos: ");
    Serial.println(numero); // Imprimir el entero recibido
  }


 String data = Serial.readStringUntil('\n'); // Leer datos hasta el carácter de nueva línea
    int numero = data.toInt(); // Convertir la cadena de texto en un entero
    motor1.write(servoPos1);
    delay(1000);
    motor1.write(numero);
    delay(1000);
}
