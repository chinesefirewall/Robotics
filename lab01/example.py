#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import the simple GoPiGo3 module
import easygopigo3 as go
# Import time
import time

#Create an instance of the robot with a constructor from the easygopigo3 module that was imported as "go".
myRobot = go.EasyGoPiGo3()

# Set speed for the GoPiGo robot in degrees per second
myRobot.set_speed(500)
# Go forward
myRobot.forward()
# Block here for 1 second
time.sleep(1)
# Start turning right
myRobot.right()
# Keep turning right for 0.5 seconds
time.sleep(0.5)
# Start moving backwards
myRobot.backward()
# Block here for 1 seconds while the robot moves backwards
time.sleep(1)
# Stop the robot
myRobot.stop()
