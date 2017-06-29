/*
   Author: Jorge Rolando Encinas
   Grupo: 10
   Materia: Agentes Inteligentes
*/

#include <SparkFun_TB6612.h>
#include <Ultrasonic.h>
#include <Clamp.h>


// these constants are used to allow you to make your motor configuration
// line up with function names like forward.  Value can be 1 or -1
const int offsetA = 1;
const int offsetB = 1;

// Pins for all inputs, keep in mind the PWM defines must be on PWM pins
#define AIN1 2
#define BIN1 7
#define AIN2 4
#define BIN2 8
#define PWMA 5
#define PWMB 6
#define STBY 9

// Pins for RPM
#define encoderLeft       A0  //    motor left encoder
#define encoderRight      A1  //    motor right encoder 

Motor motor1(AIN1, AIN2, PWMA, offsetA, STBY);
Motor motor2(BIN1, BIN2, PWMB, offsetB, STBY);

Ultrasonic ultrasonic(12, 13);

Clamp clamp;
static int serialMsg = 0;
int pinza = 0;

// vars for setup encoders for angles
int previousDigitalLeft = digitalRead(encoderLeft);
int previousDigitalRight = digitalRead(encoderRight);
int digitalLeft;
int digitalRight;
// vars for angle events
int encoderCountLeft = 0;
int encoderCountRight = 0;
int speedLeft = 0;
int speedRight = 0;
int pointsLeft = 0;
int pointsRight = 0;
// end of vars of angles
String report;

void setup() {
  Serial.begin(38400);
  clamp.attach(10);
  motor1.brake();
  motor2.brake();
  Serial.print("$I,OK");
}

void loop() {
  updateEventListener();
  updateAngle();
  updateClamp();
}

void updateAngle(){
  digitalLeft = digitalRead(encoderLeft);
  if (digitalLeft != previousDigitalLeft) {
    encoderCountLeft++;
    previousDigitalLeft = digitalLeft;
    Serial.print("$L,");
    Serial.println(encoderCountLeft);
  }
  digitalRight = digitalRead(encoderRight);
  if (digitalRight != previousDigitalRight) {
    encoderCountRight++;
    previousDigitalRight = digitalRight;
    Serial.print("$R,");
    Serial.println(encoderCountRight);
  }
  if (encoderCountLeft < pointsLeft) //40 es
    motor1.drive(speedLeft);
  else
    motor1.brake();
  if (encoderCountRight < pointsRight) //40 es
    motor2.drive(speedRight);
  else
    motor2.brake();
}

void updateClamp() {
  if (pinza == 0)
    clamp.setValue(100);
  else
    clamp.setValue(0);
  //  clamp.setValue(1*100);
}

void example2() {
  motor1.drive(30, 1000);
  motor1.brake();
  motor1.drive(-30, 1000);
  motor1.brake();
  delay(1000);
}

void updateUltrasonic() {
  Serial.print("$U,");
  Serial.println(ultrasonic.distanceRead());
}

void updateEventListener() {
  if (Serial.available() > 0) {
    delay(4);
    serialMsg = Serial.read(); //$
    if (serialMsg == '$') {
      serialMsg = Serial.read();
      switch (serialMsg) {
        Serial.read();
        case 'A': // Angulos o avances
          encoderCountLeft = 0;
          speedLeft = Serial.parseInt() * 255/100;
          Serial.read(); // ','
          pointsLeft = Serial.parseInt();
          encoderCountRight = 0;
          speedRight = Serial.parseInt() * 255/100;
          Serial.read(); // ','
          pointsRight = Serial.parseInt();
          break;
        case 'P': // Pinza
          pinza = Serial.parseInt();
          break;
        case 'U': // Ultrasonic
          updateUltrasonic();
          break;
        case 'e': // Test
          break;
        default:
          Serial.print("No case found: '");
          Serial.print(char(serialMsg));
          Serial.println("'");
          break;
      }
    }
  } else {
    ;//updateUltrasonic();
  }
}

