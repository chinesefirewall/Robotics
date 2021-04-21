
#include <Servo.h>

//initializes servo
Servo myservo;

//initializes default speed

int speedo = 1500;
int servo_speed = 1600;
int history_speed = 1600;

//keeps track on how often motion is detected
int counter = 0;

//pir variables
const int pirPin = 5;         
int state = 0;



void setup() {
  // setup code:
  Serial.begin(9600);         // initialize serial 
  pinMode(pirPin, INPUT);     // input from PIR
  // set the digital pin as output:
  myservo.attach(9); //servo digital pin
  myservo.writeMicroseconds(1500);

}

void loop() {
  //read in serial input
     if (Serial.available()>0){
       int input = Serial.parseInt();
       
       //check tresholds
       if ((input >= 1400) and (input <= 1600)){

          //set the current rotator speed 
          servo_speed = input;

         //set new history speed
         if(counter==1){
          //history_speed = servo_speed;
          //speedo = servo_speed;
         }        
       }}


  //------------switch on or off --------------

  if(digitalRead(pirPin) == HIGH  &&  state == 0){
    Serial.println("Motion detected!");
    state = 1;

    if (counter==0){
        history_speed = servo_speed;
    }    
    counter = counter + 1;
  }
    
  if(digitalRead(pirPin) == LOW  &&  state == 1){
    Serial.println("No movement any more");
    state = 0;
  }
  
  //when motion detected again restore movement according to history speed
  if(counter == 2){
    //speedo = history_speed;
    counter = 0;   
  }
//send value to servo
myservo.writeMicroseconds(servo_speed);


//loop delay
delayMicroseconds(20);
    
}
