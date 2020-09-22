// The code blinks the center LED in the dot matrix.

// Defining row pins for ease of use.
// You should enter the pin numbers that you connected your display to.
int R1 = ENTER PIN NR HERE;
int R2 = ENTER PIN NR HERE;
int R3 = ENTER PIN NR HERE;
int R4 = ENTER PIN NR HERE;
int R5 = ENTER PIN NR HERE;
int R6 = ENTER PIN NR HERE;
int R7 = ENTER PIN NR HERE;

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

// For start turn all the LED's off in the column.
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
}
