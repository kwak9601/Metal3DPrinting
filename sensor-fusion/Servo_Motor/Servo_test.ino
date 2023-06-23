#include <Servo.h>
int servoPin = 9;
int servoPos = 270;
Servo myServo;


void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
myServo.attach(servoPin);

}

void loop() {
myServo.write(servoPos);
}
