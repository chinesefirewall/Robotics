// initialization and module import
////////////////////////////////////
#include <Servo.h>
Servo my_servo;
int angle;
int degree;
int state;
//////////////////////////////////
void setup()  {
    // SETUP CODE
    my_servo.attach(11);
    Serial.begin(9600);
    //degree = 1;
    state = 0;
    angle = 0;
}

// loop
void loop() {
  if (state == 0) { my_servo.write(angle);
    angle++; // increament by 1
    }
    if (angle == 180) {
      state = 1;
      } 
    
   if (state == 1) {
      my_servo.write(angle);
      angle--; //  decreament by 1
      }
      if (angle == 0) {
        state = 0;
    }

    delay(10);
}
