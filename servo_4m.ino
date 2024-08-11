#include<Servo.h>
int MeniquePin = 3;
int MeniquePos = 0;//el angulo del servo motor
Servo Menique;//Nombre del servo motor

int AnularPin = 5;
int AnularPos = 0;//el angulo del servo motor
Servo Anular;//Nombre del servo motor

int CorazonPin = 6 ;
int CorazonPos = 0;
Servo Corazon;//Nombre del servo motor

int IndicePin = 9;
int IndicePos = 0;
Servo Indice;//Nombre del servo motor

/*int servoPin5 = 10;
int servoPos5 = 0;
Servo miniservo; //Nombre del servo motor
*/
void setup(){
  Menique.attach(MeniquePin);

  Anular.attach(AnularPin);

  Corazon.attach(CorazonPin);

   Indice.attach(IndicePin);
  
  Serial.begin(9600);
}

void loop(){
 Menique.write( MeniquePos);
 
delay(1000);

 Anular.write( AnularPos);

delay(1000);

Corazon.write(CorazonPos);

delay(1000);

Indice.write(IndicePos);

delay(1000);

delay(2000);

 Menique.write(180);
 
delay(2000);

 Anular.write(180);

delay(2000);

Corazon.write(180);

delay(2000);

Indice.write(180);

delay(2000);


}
