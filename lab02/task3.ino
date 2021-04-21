// Datasheet for Ultrasonic Ranging Module HC - SR04
// https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf

int echo_pin = 2;
int trig_pin = 3;
int delay_us = 50; // <--- YOU HAVE TO FIND THE CORRECT VALUE FROM THE DATASHEET
long distance_mm = 0;
long duration_us;

void setup()  {
    // YOUR SETUP CODE GOES HERE
    // In this section you should initialize serial connection to Arduino
    // and set echo_pin and trig_pin to correct modes
}

void loop() {
    // To generate the ultrasound we need to
    // set the trig_pin to HIGH state for correct ammount of µs.
    digitalWrite(trig_pin, HIGH);
    delayMicroseconds(delay_us);
    digitalWrite(trig_pin, LOW);
    
    // Read the pulse HIGH state on echo_pin
    // the length of the pulse in microseconds
    duration_us = pulseIn(echo_pin, HIGH);
    
    // YOU HAVE TO CALCULATE THE distance_mm BASED ON THE duration_us
    // FIND THE FORMULA FROM THE DATASHEET AND IMPLEMENT IT HERE
    
    Serial.println(distance_mm);
    
    delay(1000);
}
