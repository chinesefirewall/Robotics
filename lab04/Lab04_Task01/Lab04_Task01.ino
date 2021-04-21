const int pir_pin = 5;           // passive infrared sensor pin
bool in_motion = false;

void setup(){
    Serial.begin(9600);          // initialize serial with 9600 baud rate
    pinMode(pir_pin, INPUT);     // set pin #5 as an input from PIR
}

void loop(){
    if(digitalRead(pir_pin) == HIGH  &&  !in_motion){
      Serial.println("Motion detected!");
      in_motion = true;
    }
    if(digitalRead(pir_pin) == LOW  &&  in_motion){
      Serial.println("No movement any more");
      in_motion = false;
    }
}
