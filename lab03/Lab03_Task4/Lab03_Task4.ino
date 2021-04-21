// The code blinks the center LED in the dot matrix.

// Defining row pins for ease of use.
// You should enter the pin numbers that you connected your display to.
int R1 = 1;
int R2 = 2;
int R3 = 3;
int R4 = 4;
int R5 = 5;
int R6 = 6;
int R7 = 7;
// int C1 = 
//int C2 = 13;
// The setup function runs once when you press reset or power the board.
void setup() {
// setting row pins as output pins.
// we can now just use the variable names for the pins that we defined above.
    pinMode(R1, OUTPUT);
    pinMode(R2, OUTPUT);
    pinMode(R3, OUTPUT);
    pinMode(R4, OUTPUT);
    pinMode(R5, OUTPUT);
    pinMode(R6, OUTPUT);
    pinMode(R7, OUTPUT);
    //pinMode(C2, OUTPUT);

//    pinMode()

// For start turn all the LED's off in the column.
    //digitalWrite(C2, HIGH);
    digitalWrite(R1, HIGH);
    digitalWrite(R2, HIGH);
    digitalWrite(R3, HIGH);
    digitalWrite(R4, HIGH);
    digitalWrite(R5, HIGH);
    digitalWrite(R6, HIGH);
    digitalWrite(R7, HIGH);
 }

// The loop function runs over and over again until the Arduino is powered on.
void loop() {
    // Write the code here to control the row pins in the desired way.
    //digitalWrite(C2,HIGH);
    digitalWrite(R1,LOW);
    delay(50);
    digitalWrite(R1, HIGH);
    

    digitalWrite(R2,LOW);
    delay(50);
    digitalWrite(R2, HIGH);

    digitalWrite(R3,LOW);
    delay(50);
    digitalWrite(R3, HIGH);

    digitalWrite(R4,LOW);
    delay(50);
    digitalWrite(R4, HIGH);

    digitalWrite(R5,LOW);
    delay(50);
    digitalWrite(R5, HIGH);

    digitalWrite(R6,LOW);
    delay(50);
    digitalWrite(R6, HIGH);

    digitalWrite(R7,LOW);
    delay(50);
    digitalWrite(R7, HIGH);
    
    // REVERSE
    

    digitalWrite(R7,LOW);
    delay(50);
    digitalWrite(R7, HIGH);
    

    digitalWrite(R6,LOW);
    delay(50);
    digitalWrite(R6, HIGH);

    digitalWrite(R5,LOW);
    delay(50);
    digitalWrite(R5, HIGH);

    digitalWrite(R4,LOW);
    delay(50);
    digitalWrite(R4, HIGH);

    digitalWrite(R3,LOW);
    delay(50);
    digitalWrite(R3, HIGH);

    digitalWrite(R2,LOW);
    delay(50);
    digitalWrite(R2, HIGH);

    digitalWrite(R1,LOW);
    delay(50);
    digitalWrite(R1, HIGH);
    //digitalWrite(C2,HIGH);

    


    
}
