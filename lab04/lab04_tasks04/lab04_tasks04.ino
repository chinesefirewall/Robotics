
//magnetometer 
#include <Wire.h>
#include <LIS3MDL.h>
LIS3MDL mag;

//pressure
#include <LPS.h>
LPS ps;

//accelometer
#include <LSM6.h>
LSM6 imu;
char report[80];

void setup() {
  Serial.begin(9600);
  Wire.begin();
  //magnetometer
  if (!mag.init())
  {
    Serial.println("Failed to detect and initialize magnetometer!");
    while (1);
  }

  mag.enableDefault();
  
  //pressure
    if (!ps.init())
  {
    Serial.println("Failed to autodetect pressure sensor!");
    while (1);
  }

  ps.enableDefault();

  //accelometer
  if (!imu.init())
  {
    Serial.println("Failed to detect and initialize IMU!");
    while (1);
  }
  imu.enableDefault();

}

void loop() {
  //  main code
//magnetometer
  mag.read();

  float x = mag.m.x/6842.0;  //  in the LIS3MDL datasheet (page 8) states a conversion factor of 6842
  float y = mag.m.y/6842.0;
  float z = mag.m.z/6842.0;

  Serial.println("M: "+String(x)+" gauss "+String(y)+" gauss "+String(z)+" gauss");
  delay(1000);

//pressure
  float pressure = ps.readPressureMillibars();
  float altitude = ps.pressureToAltitudeMeters(pressure);
  float temperature = ps.readTemperatureC();
  
  Serial.print("pressure: ");
  Serial.print(pressure);
  Serial.print(" mbar\ta: ");
  Serial.print(altitude);
  Serial.print(" m\tt: ");
  Serial.print(temperature);
  Serial.println(" degree Celcius");

  delay(1000);

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
  float imuaz = imu.a.z*0.000061;

  float imugx = imu.g.x*0.00875;
  float imugy = imu.g.y*0.00875;
  float imugz = imu.g.z*0.00875;

// -----------------------------------------
Serial.print("accelerometer: ");
Serial.print(imuax);
Serial.print(" g-units ");

//Serial.print("accelerometer: ");
Serial.print(imuay);
Serial.print(" g-units ");

//Serial.print("accelerometer: ");
Serial.print(imuaz);
Serial.print(" g-units \n");


Serial.print("gyroscope: ");
Serial.print(imugx);
Serial.print(" DPS ");


//Serial.print("gyroscope: ");
Serial.print(imugy);
Serial.print(" DPS ");


//Serial.print("gyroscope: ");
Serial.print(imugz);
Serial.print(" DPS \n");

// -----------------------------------------

  delay(1000);

}
