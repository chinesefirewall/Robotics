//NB: code still under construction

// initialization and module import
////////////////////////////////////
#include <Servo.h>
Servo my_servo;
int angle;
//////////////////////////////////
void setup()  {
    // YOUR SETUP CODE
    my_servo.attach(11);
    Serial.begin(9600);
 
    
}
// loop
void loop() {
    angle = 60;
    my_servo.write(angle);
    if (angle < 180) {
      angle +=1;
     else if (angle = 180) {angle -=1
      }
      }
     


    
    delay(1000);
}

/////////////////////////////  below codes are not part of solution, they are just for my personal reference  /////////////////////////////////////////

void setup()
{
  // the 1000 & 2000 set the pulse width 
  // mix & max limits, in microseconds.
  // Be careful with shorter or longer pulses.
  testservo.attach(9, 1000, 2000);

  next = millis() + 500;
}

void loop()
{
  static bool rising = true;

  if(millis() > next)
  {
    if(rising)
    {
      testservo.write(180);
      rising = false;
    }
    else
    {
      testservo.write(0);
      rising = true;
    }

    // repeat again in 3 seconds.
    next += 3000;
  }

}
