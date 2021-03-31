#include <Servo.h>
Servo servo1;
Servo servo2;

#define OFFMODE -1
#define ONMODE 1

char ch;
int state = OFFMODE;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servo1.attach(7);
  servo2.attach(8);
  servo1.write(0);
  servo2.write(0);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    ch = Serial.read();
  }
  if(ch=='a'){
    servo1.write(90);
    servo2.write(90);
  }else if(ch=='b'){
    servo1.write(0);
    servo2.write(0);
  }
}
