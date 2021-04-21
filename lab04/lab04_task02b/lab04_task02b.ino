
#include <Servo.h>

//initializes servo
Servo myservo;

//initializes default speed, which is basically standing point
int speedo = 1500;

int history_speed = 1500;

//keeps track on how often motion is detected
int counter = 0;

//pir variables
const int pirPin = 5;         // passive infrared sensor pin
int state = 0;                // 0 - no motion, 1 - motion detect


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);         // initialize serial with 9600 baud rate
  pinMode(pirPin, INPUT);     // set pin #5 as an input from PIR
  // set the digital pin as output:
  myservo.attach(9); //servo digital communication pin initialization
  myservo.writeMicroseconds(1500);  // set servo to mid-point

}

void loop() {
  //read in serial input
     if (Serial.available()>0){
       int input = Serial.parseInt();
       
       //check if input is in needed tresholds
      if ((input >= 1400) and (input <= 1600)){

          //set the current rotator speed 
          speedo = input;

         //set new history speed if valid value is entered while motion is stopped and keep current motion as STOP
         if(counter==1){
          history_speed=speedo;
          speedo = 1500;
         }        
       }}


  //------------switch on or off --------------

  if(digitalRead(pirPin) == HIGH  &&  state == 0){
    Serial.println("Motion detected!");
    state = 1;

    if (counter==0){

        history_speed = speedo;
        speedo = 1500;
    }    
    counter = counter + 1;
  }
    
  if(digitalRead(pirPin) == LOW  &&  state == 1){
    Serial.println("No movement any more");
    state = 0;
  }
  
  //when motion detected again restore movement according to history speed
  if(counter == 2){

    speedo = history_speed;
    counter = 0;   
  }
//send value to servo
myservo.writeMicroseconds(speedo);

//loop delay to allow servo current command completion
delayMicroseconds(20);
    
}
