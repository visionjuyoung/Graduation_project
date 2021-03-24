#include <Servo.h>
Servo servo;

#define OFFMODE -1
#define ONMODE 1

char ch;
int state = OFFMODE;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servo.attach(7);
  servo.write(0);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    ch = Serial.read();
  }
  if(ch=='a'){
    servo.write(90);
  }else if(ch=='b'){
    servo.write(0);
  }
}
