#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import time
import easygopigo3 as go
import read_sensors as sensors
import sys

def follow(robot, ls1, ls2, ls3, ls4, ls5, us):

    """
    TASK: Code for following the line based on line sensor readings
    """
    if ls5==0:
        robot.set_motor_dps(robot.MOTOR_LEFT,50)
        robot.set_motor_dps(robot.MOTOR_RIGHT,50)
        #mark_counter = mark_counter + 1
        

        
    if ls4==0:
        robot.set_motor_dps(robot.MOTOR_LEFT,60)
        robot.set_motor_dps(robot.MOTOR_RIGHT,20)
    
    if ls3==0:
        robot.set_motor_dps(robot.MOTOR_LEFT,60)
        robot.set_motor_dps(robot.MOTOR_RIGHT,60)
    
    if ls2==0:
        robot.set_motor_dps(robot.MOTOR_LEFT,20)
        robot.set_motor_dps(robot.MOTOR_RIGHT,60)

    if ls1==0:
#         robot.set_motor_dps(robot.MOTOR_LEFT,20)
#         robot.set_motor_dps(robot.MOTOR_RIGHT,60)
        print('-------------------sensor 1------------------')
#     if markers_count >= 7:
#         robot.drive_cm(5)
#         robot.stop()
#     
    print(' mark counter = ', markers_count)
    return

def markers_detected(ls1, markers_count, us):
    global on_marker
    """
    TASK: Code for detecting markers, update markers_count if needed
    """
    if ls1 == 0 and on_marker == False:
        on_marker = True
        print('----------- Marker detected --------')
        markers_count += 1
        if markers_count == 1:
            print("distance  of mark 1 to finish line is  ----------------->   1800 mm")
        elif markers_count == 2:
            print("distance  of mark 2 to finish line is  ----------------->   1600 mm")
        elif markers_count == 3:
            print("distance  of mark 3 to finish line is  ----------------->    1380 mm")
        elif markers_count == 4:
            print("distance  of mark 4 to finish line is  ----------------->   1100 mm")
        elif markers_count == 5:
            print("distance  of mark  5 to finish line is  ----------------->   700 mm")    
        elif markers_count == 6:
            print("distance  of mark 6 to finish line is  ----------------->    400 mm")  
        elif markers_count == 7:
            print("distance of mark 7 to finish line is ----------------->    200 mm")
# '''
# for self consuption again next lab
# line 1 is 1800 cm from finish line
# line 7 is 200 cm from finish
# 
# every other thing works
# '''
        
    elif ls1 == 1:
        on_marker = False
        
     
#     print('Numbers of markers', markers_count )
    return markers_count


def close(message=""):
    """
    line_following specific cleanup function
    """
    global running, ser, robot
    print(message)
    running = False
    robot.stop()
    if ser.is_open:
        ser.close()
    sys.exit(0)


def signal_handler(sig, frame):
    """
    This function will be called when CTRL+C is pressed
    """
    close('\nYou pressed Ctrl+C! Closing the program nicely :)')


if __name__ == "__main__":
    # Register a callback for CTRL+C
    signal.signal(signal.SIGINT, signal_handler)

    robot = go.EasyGoPiGo3()
    robot.set_speed(100)

    running, ser = sensors.initialize_serial('/dev/ttyUSB1')
#     arduino_data = get_data_from_arduino(ser)

    markers_count = 0 # Change to correct value
    on_marker = False
    while running:
        arduino_data = sensors.get_data_from_arduino(ser)
#         arduino_data = get_data_from_arduino(ser)

        if arduino_data:
            # Extract the sensor values
            ls1 = arduino_data['ls1']
            ls2 = arduino_data['ls2']
            ls3 = arduino_data['ls3']
            ls4 = arduino_data['ls4']
            ls5 = arduino_data['ls5']
            us = arduino_data['us']

            # Print received to the console
            print("LS1: ", ls1, "LS2: ", ls2, "LS3: ", ls3, "LS4: ", ls4, "LS5: ", ls5, "US: ", us)
            
            markers_count = markers_detected(ls1, markers_count, us)
            follow(robot, ls1, ls2, ls3, ls4, ls5, us)
            
            #############
               
        
        if markers_count >= 7 and us <= 500:
            robot.stop()
            break


        if not ser.is_open:
            close("Serial is closed!")

        # Throttle the loop to about 10 times per second
        time.sleep(.1)
        ###########################################
#         arduino_data = sensors.get_data_from_arduino(ser)
#         if arduino_data:
#             ls1 = arduino_data['ls1']
#             ls2 = arduino_data['ls2']
#             ls3 = arduino_data['ls3']
#             ls4 = arduino_data['ls4']
#             ls5 = arduino_data['ls5']
#             us = arduino_data['us']
#             print("LS1: ", ls1, "LS2: ", ls2, "LS3: ", ls3, "LS4: ", ls4, "LS5: ", ls5,  "US: ", us )
# 
#             markers_count = markers_detected(ls1, markers_count, us)
#             follow(robot, ls1, ls2, ls3, ls4, ls5, us)
#             
#             #############
#                
#         
#         if markers_count >= 7 and us <= 500:
#             robot.stop()
#             break
# 
#         if not ser.is_open:
#             close("Serial is closed!")
# 
#         # Throttle the loop to 50 times per second
#         time.sleep(.02)
#         close()
    