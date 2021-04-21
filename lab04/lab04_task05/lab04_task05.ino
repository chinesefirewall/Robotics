// servo module
#include <Servo.h>

////magnetometer module 
#include <Wire.h>

#include <LIS3MDL.h>

//accelometer module
#include <LSM6.h>

//pressure module
#include <LPS.h>

//initializes servo
Servo myservo; // call as myservo
int servo_speed = 1500;  // initializing servo to mid point

////magnetometer module 
LIS3MDL mag; // call as mag

//pressure module
LPS ps;  // call as ps

LSM6 imu;  // call as imu


void setup() {
  //servo init  
  myservo.attach(9); //servo digital pin initialization to pin 9 on arduino
  myservo.writeMicroseconds(1500);  // mid-point for servo
  
  Serial.begin(9600);
  Wire.begin();
  //magnetometer -  safety net
  if (!mag.init())
  {
    Serial.println("Failed to detect and initialize magnetometer!");
    while (1);
  }

//  mag.enableDefault();
//  
//  //pressure -  safety net
//    if (!ps.init())
//  {
//    Serial.println("Failed to autodetect pressure sensor!");
//    while (1);
//  }

//  ps.enableDefault();

  //accelometer  -  safety net
  if (!imu.init())
  {
    Serial.println("Failed to detect and initialize IMU!");
    while (1);
  }
  imu.enableDefault();

}

void loop() {
  // main code run repeatedly in loop
//magnetometer
  mag.read();
  float x = mag.m.x/6842.0;   //  in the LIS3MDL datasheet (page 8) states a conversion factor of 6842
  float y = mag.m.y/6842.0;
  float z = mag.m.z/6842.0;

  // printing mag value to serial board
  Serial.println("M: "+String(x)+" gauss "+String(y)+" gauss "+String(z)+" gauss ");

////pressure
//  float pressure = ps.readPressureMillibars();
//  float altitude = ps.pressureToAltitudeMeters(pressure);
//  float temperature = ps.readTemperatureC();
//  
//  Serial.print("p: ");
//  Serial.print(pressure);
//  Serial.print(" mbar\ta: ");
//  Serial.print(altitude);
//  Serial.print(" m\tt: ");
//  Serial.print(temperature);
//  Serial.println(" degree Celcius ");


//accelometer
/* 
LA_So specification in the LSM6DS33 datasheet (page 11)
states a conversion factor of 0.061 mg/LSB (least
significant bit) at this FS setting, so the raw reading of
16276 corresponds to 16276 * 0.061 = 992.8 mg = 0.9928 g.
*/
  imu.read();

  float imuax = imu.a.x*0.000061;
  float imuay = imu.a.y*0.000061;
  float imuaz = imu.a.z*0.0061;

  float imugx = imu.g.x*0.00875;
  float imugy = imu.g.y*0.00875;
  float imugz = imu.g.z*0.00875;

// --------------------------------------------

//Serial.print("accelerometer: ");
//Serial.print(imuax);
//Serial.print(" g-units ");
//
////Serial.print("accelerometer: ");
//Serial.print(imuay);
//Serial.print(" g-units ");

//Serial.print("accelerometer: ");
Serial.print(imuaz);
Serial.print(" <------ LOOK HERE g-units \n");

//
//Serial.print("gyroscope: ");
//Serial.print(imugx);
//Serial.print(" DPS ");
//
//
////Serial.print("gyroscope: ");
//Serial.print(imugy);
//Serial.print(" DPS ");


//Serial.print("gyroscope: ");
Serial.print(imugz);
Serial.print(" DPS \n");

delay(1000);


//  ---------------------------------------------
// map(value, fromLow, fromHigh, toLow, toHigh)

servo_speed = map(imuaz,-100,100,1400,1600);
myservo.writeMicroseconds(servo_speed);
}

/*
 * Parameters
value: the number to map.
fromLow: the lower bound of the value’s current range.
fromHigh: the upper bound of the value’s current range.
toLow: the lower bound of the value’s target range.
toHigh: the upper bound of the value’s target range.

*/
