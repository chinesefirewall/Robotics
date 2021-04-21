const int pir_pin = 5;          
const int ledPin =  LED_BUILTIN;

bool in_motion = false;
int ledState = LOW; 
unsigned long previousMillis = 0;  
const long interval = 200;
bool blinking = false;

void setup(){
    Serial.begin(9600);         
    pinMode(pir_pin, INPUT);     
    pinMode(ledPin, OUTPUT);
}

void loop(){
  unsigned long currentMillis = millis();
  if(digitalRead(pir_pin) == HIGH  &&  !in_motion){
      Serial.println("Motion detected!");
      in_motion = true;
      if (blinking == true){
        ledState = LOW;
        blinking = false;
        digitalWrite(ledPin, ledState);
      }
      else {
        blinking = true;
      }
    }
    
  if(digitalRead(pir_pin) == LOW  &&  in_motion){
    Serial.println("No movement anymore");
    in_motion = false;
    }
    
  if (blinking == true){ 
    if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;
      if (ledState == LOW) {
        ledState = HIGH;
      } else {
        ledState = LOW;
      }
      digitalWrite(ledPin, ledState);
    }
  }
}
