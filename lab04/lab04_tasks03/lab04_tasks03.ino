
// ----------------------------------------------------



#include <Servo.h>

//initializes servo
Servo myservo;

//initializes default speed

int servo_speed = 1600;

//pir variables
const int pirPin = 5;

//===assign threshold values for RPM calculation
float rpm = 0;
int maxo = 120;
int lowo = 40;

const long interval = 0; 
unsigned long previous_time = 0;   

bool in_shade = true; 

void setup() {
  // setup code:

  Serial.begin(9600);         // initialize serial 
  pinMode(pirPin, INPUT);     // input from PIR
  // set the digital pin as output:
  myservo.attach(9); //servo digital pin
  myservo.writeMicroseconds(1500);

}

void loop() {


  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);

//  if (sensorValue >= maxo &&  in_shade){bool shade = false;
  if (sensorValue >= maxo &&  !in_shade){
    long current_time = millis();
    long interval = current_time - previous_time;
// ------------------------ RPM conversion here ----------------------------
   float minut = interval / 1000.0;
   float hold = 1/minut;
   float holder = hold * 60;
    
    Serial.println(holder);
//    if (current_time - previous_time >= interval) {
      previous_time = current_time;
//      }
//    Serial.println(interval);
    current_time = 0;
    in_shade = true;
  
  
    }
  //if (sensorValue <= lowo &&  in_shade) {bool shade = true;
  if (sensorValue <= lowo &&  in_shade) {
    long previous_time = millis();
    //Serial.println(previous_time);
    in_shade = false;
    previous_time = 0;
  }


  
  // print out the value you read:
  //Serial.println(sensorValue);
  
  
  //read in serial input
     if (Serial.available()>0){
       int input = Serial.parseInt();
       
       //check tresholds
       if ((input >= 1400) and (input <= 1600)){

          //set the current rotator speed 
          servo_speed = input;

       }}


    //send value to servo
    myservo.writeMicroseconds(servo_speed);

//loop delay
delayMicroseconds(20);
delay(10);        // delay in between reads for stability

    
}
