#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## all imports needed
import collections
import cv2
import easygopigo3 as go
import numpy as np
import time



def updatelH(new_value):
  global hH, hS, hV, lH, lS, lV
  lH = new_value
  return

def updatehH(new_value):
  global hH, hS, hV, lH, lS, lV
  hH = new_value
  return

def updatelS(new_value):
  global hH, hS, hV, lH, lS, lV
  lS = new_value
  return

def updatehS(new_value):
  global hH, hS, hV, lH, lS, lV
  hS = new_value
  return


def updatelV(new_value):
  global hH, hS, hV, lH, lS, lV
  lV = new_value
  return


def updatehV(new_value):
  global hH, hS, hV, lH, lS, lV
  hV = new_value
  return

def updateKernelValue(new_value):
  global kernel_size
  kernel_size = new_value

## Declare all variables
image_center = 640
integral = 0
previous = 0
# state
see_line = False

lH = 77
hH = 95
lS = 58
hS = 231
lV = 89
hV = 161
kernel_size = 0
# kernel initializerone

# Global variable for determining GoPiGo speed.
gospeed = 450

# Global variable for video feed.
cap = None

# Global variable for robot object.
my_robot = go.EasyGoPiGo3()

cv2.namedWindow('Processed')
cv2.createTrackbar("Low H", 'Processed', lH, 255, updatelH)
cv2.createTrackbar("High H", 'Processed', hH, 255, updatehH)
cv2.createTrackbar("Low S", 'Processed', lS, 255, updatelS)
cv2.createTrackbar("High S", 'Processed', hS, 255, updatehS)
cv2.createTrackbar("Low V", 'Processed', lV, 255, updatelV)
cv2.createTrackbar("High V", 'Processed', hV, 255, updatehV)
cv2.createTrackbar("Kernel size", 'Processed', kernel_size, 100, updateKernelValue)

def init():
    global cap, gospeed, lowerThresh , upperThresh ,hH, hS, hV, lH, lS, lV, kernel
    # This function should do everything required to initialize the robot.
    # Among other things it should open the camera and set GoPiGo speed.
    # Some of this has already been filled in.
    # You are welcome to add your own code if needed.

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# limit for thresh
    lowerThresh = np.array([lH, lS, lV])
    upperThresh = np.array([hH, hS, hV])
    
    my_robot.set_speed(gospeed)
    kernel = np.ones((3,3), dtype = np.uint8)
    return

# TASK 1
def get_line_location(frame):
    # This function should use a single frame from the camera to determineq line location.
    # It should return the location of the line in the frame.
    # Feel free to define and use any global variables you may need.
    # YOUR CODE HERE
### function should take in a thresholded image and work on tqhe non zero values
    
    location_value = np.nonzero(frame) # non zero values will mbe the location of line
    location_of_line = np.mean(location_value[1])  # arithmetic mean will be the center of the line
    print('loc of line ',location_of_line)
    return location_of_line

# TASK 2
def bang_bang(linelocation):
    # This function should use the line location to implement a simple bang-bang controller.
    # YOUR CODE HERE
    global image_center
    
# #     bang bang control is fast and simple but wont be able to handle complex taska
    adjustment = image_center - linelocation
#     print('adjustment  ', adjustment)
#     print('linelocation  ', linelocation)
    print('image_center  ', image_center)

    if adjustment < 0:
        my_robot.right()
        print('forward')
    else:
        my_robot.left()
        print('turn left')
    return

# TASK 3
def bang_bang_improved(linelocation):
    # This function should use the line location to implement an improved version of the bang-bang controller.
    # YOUR CODE HERE

    global image_center
    adjustment = image_center - linelocation
    print('image_center  ', image_center)
    try:
## # if the adjustment is too wide, then it doesnt follow line
## if too small it won;t go into the else statment also
        if adjustment < -500:
            my_robot.right()
            print('turn right')
        elif adjustment > 500:
            my_robot.left()
            print('turn left')
        else:
            my_robot.forward()
            print('move foward ')
    except:
        print('no line detected ---- turn around')
        my_robot.steer(70,90)
    return

# TASK 4
def proportional_controller(linelocation):
    # This function should use the line location to implement a proportional controller.
    # Feel free to define and use any global variables you may need.
    # YOUR CODE HERE
    global image_center
    try:
    
            
        error_of_location = image_center - linelocation # diff btw center of the camera and center of the line
        prop_constant_P = int(0.6 * error_of_location)
        controller_output =  prop_constant_P
        
        print('controller_output  ', prop_constant_P)
        print('error_of_location  ', error_of_location)
        print('image_center  ', image_center)
         
        my_robot.set_motor_dps(my_robot.MOTOR_LEFT,gospeed-controller_output)
        my_robot.set_motor_dps(my_robot.MOTOR_RIGHT,gospeed+controller_output)
        
##### ----------------- Over kill implemntation ---------------
#         if error_of_location < -100:
#                 
#             my_robot.set_motor_dps(my_robot.MOTOR_LEFT,gospeed-controller_output)
#             my_robot.set_motor_dps(my_robot.MOTOR_RIGHT,gospeed+controller_output)
#             
#             print('turn right')
#         elif error_of_location > 100:
#             my_robot.set_motor_dps(my_robot.MOTOR_LEFT,gospeed-controller_output)
#             my_robot.set_motor_dps(my_robot.MOTOR_RIGHT,gospeed+controller_output)
#             
#             print('turn left')
#         else:
#             my_robot.forward()
#             print('move foward ')
    except:
        print('no line detected ---- STOP')
        my_robot.stop()
        time.sleep(1000)
            
    return


# TASK 5
def pid_controller(linelocation):
    
    # This function should use the line location to implement a PID controller.
    # Feel free to define and use any global variables you may need.
    # YOUR CODE HERE
    global Kd, Ki, Kp, previous, integral
    try:
    
        error_of_location = image_center - linelocation # diff btw center of the camera and center of the line
        speed = int(0.2 * error_of_location)
        
        integral = integral + error_of_location
        
        derivative = error_of_location - previous
        previous = error_of_location
        PID_controller = Kp * error_of_location + Ki * integral + Kd * derivative
        
        
        print('PID_controller  ', PID_controller)
        print('derivative  ', derivative)
        print('speed  ', speed)
         
        my_robot.set_motor_dps(my_robot.MOTOR_LEFT,gospeed-PID_controller)
        my_robot.set_motor_dps(my_robot.MOTOR_RIGHT,gospeed+PID_controller)
    except:
        my_robot.drive_cm(10)

    return


# Initialization
init()

#current time of capture
start_time = time.time()
# x1 = 400
# y1 = 800

Tu = 32 # should be btw 10 and 15
Ku = 1.2 # should be btw 1.2 and 1.5
Kp = 0.6*Ku
Ki = (1.2*Ku)/Tu
Kd = (3*Tu*Ku)/40


try:
    while True:
        
        
        # We read information from the camera.
        ret, frame = cap.read()
        
        frame = frame[550:600,0:1280]
        
         
        ##FPS
        current_time = time.time()
        diff = (current_time - start_time)
        start_time = current_time
        # Write some text onto the frame (FPS number)
        
        cv2.putText(frame, str(np.floor(1 / diff)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
#         cv2.imshow('Original', frame)
        HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
       
        lowerThresh = np.array([lH, lS, lV])
        upperThresh = np.array([hH, hS, hV])
        ##THRESHOLD image_center
        
#         frame_blurred = cv2.GaussianBlur(frame, (1 + 2 * kernel_size, 1 + 2 * kernel_size), 0)
 
        thresh = cv2.inRange(HSV,lowerThresh , upperThresh )
        cv2.putText(thresh, str(np.floor(1 / diff)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 100), 2)
        cv2.imshow('Original', thresh)
        
#         Task 1: uncomment the following line and implement get_line_location function.
        linelocation = get_line_location(thresh)
        #print('center of line is:  ', linelocation)
        
        # Task 2: uncomment the following line and implement bang_bang function.
#         bang_bang(linelocation)

        # Task 3: uncomment the following line and implement bang_bang_improved function.
#         bang_bang_improved(linelocation)

        # Task 4: uncomment the following line and implement proportional_controller function.
#         proportional_controller(linelocation)

        # Task 5: uncomment the following line and implement pid_controller function.
        pid_controller(linelocation)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    cap.release()
    cv2.destroyAllWindows()
    my_robot.stop()

cap.release()
cv2.destroyAllWindows()
my_robot.stop()
