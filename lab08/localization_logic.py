#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import easygopigo3 as go
import time
import signal
import cv2
import threading
import line_following as line
import numpy as np
import read_sensors as sensors
from visualisation import RepeatTimer
import sys



blobparams = cv2.SimpleBlobDetector_Params()
blobparams.filterByConvexity = False
blobparams.minDistBetweenBlobs = 1000
blobparams.minArea = 50
blobparams.filterByColor = False
blobparams.maxArea = 20000000
blobparams.filterByInertia = False
blobparams.filterByArea = True
blobparams.filterByCircularity = False

## HSV threshold values  from thresholder.py 94 255 168 255 84 256
lH = 94
hH = 255
lS = 168
hS = 255
lV = 84
hV = 256
# kernel_size = 0


# Dictionary for holding positions
positions = {'current_marker': -1, 'current_us': -1, 'current_enc': -1, 'current_cam': -1}


def fast_worker(running, robot, positions, ser, close_function):
    """
    Fastworker logic
    A while-loop with the main control logic and should be used for fast processes.
    """

    print("Starting fastWorker in a separate thread")

    # Distance from the START marker to the wall in mm
    start_to_wall_dist = 1800

    last_ls1 = 0
#     markers_count = 0
    on_marker = False
    robot.reset_encoders()
    marker_state = False
    
    while running:
        arduino_data = sensors.get_data_from_arduino(ser)

        """
        TASK: Get the averaged encoder value and use it to
        find the distance from the wall in millimetres
        positions['current_enc'] = ...
        """

        if arduino_data:
            ls1 = arduino_data['ls1']
            ls2 = arduino_data['ls2']
            ls3 = arduino_data['ls3']
            ls4 = arduino_data['ls4']
            ls5 = arduino_data['ls5']
            us_pos = arduino_data['us']
            

            """
            TASK: save current ultrasonic position to positions dictionary
            """
            encoder_value = robot.read_encoders_average()
#             print('encoder value ---> ', encoder_value)
            
            positions['current_us'] = us_pos
            positions['current_marker'], on_marker = line.markers_detected(ls1,positions['current_marker'], last_ls1, on_marker)
#             remaining_dist = start_to_wall_dist - encoder_value*10
#             positions['current_enc'] = remaining_dist
#             

            """
            Add the rest of your line following & marker detection logic
                """
#             positions['current_marker'] = line.markers_detected(ls1, last_ls1,us_pos, on_marker)
#             print('# ---------------- remaining_dist to wall  ------------->   ',positions['current_marker'])
            if positions['current_marker'] == 1 and marker_state == False:
                robot.reset_encoders()
                marker_state = True
                start_to_wall_dist = 1800
                
            elif positions['current_marker'] == 2 and marker_state == True:
                robot.reset_encoders()
                start_to_wall_dist = 1600
                marker_state = False
            elif positions['current_marker'] == 3 and marker_state == False:
                robot.reset_encoders()
                start_to_wall_dist = 1380
                marker_state = True
            elif positions['current_marker'] == 4 and marker_state == True:
                robot.reset_encoders()
                start_to_wall_dist = 1100
                marker_state = False
            elif positions['current_marker'] == 5 and marker_state == False:
                robot.reset_encoders()
                start_to_wall_dist = 700
                marker_state = True
            elif positions['current_marker'] == 6 and marker_state == True:
                robot.reset_encoders()
                start_to_wall_dist = 400
                marker_state = False
            elif positions['current_marker'] == 7:
                start_to_wall_dist = 200
                robot.stop()

            else:
                line.follow(robot, ls1, ls2, ls3, ls4, ls5, us_pos)
                
            remaining_dist = start_to_wall_dist - encoder_value*10
            positions['current_enc'] = remaining_dist
                
                

        if not ser.is_open:
            close_function("Serial is closed!")

        # Limit control thread to 50 Hz
        time.sleep(0.02)

    close_function("Fast_worker closed!")

detector = cv2.SimpleBlobDetector_create(blobparams)
def detect_blobs(frame):
    global detector
    
  ## HSV threshold values  from thresholder.py 94 255 168 255 84 256
    lH = 94
    hH = 255
    lS = 168
    hS = 255
    lV = 84
    hV = 256
        
    
    lowerLimits = np.array([lH, lS, lV])
    upperLimits = np.array([hH, hS, hV])
    """Image processing and blob detection logic"""
    
    # Our operations on the frame come here
    HSV_img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    thresholded = cv2.inRange(HSV_img, lowerLimits, upperLimits)
    thresholded = 255 - thresholded

#     detector = cv2.SimpleBlobDetector_create(blobparams)
    keypoints = detector.detect(thresholded)
    
    
    for keys in keypoints:
        size = keys.size
        print('Diameter is------------------>', round(size)) # to  confirm the blob size detection
    
    

    return keypoints

### --------------------------------------------------------------- begining of insertion -----------------------------------------------------

    
def get_blob_size(keypoints):
   
        
    """Find the size of biggest keypoint    """
    max_size = 0
    for keys in keypoints:
        if keys.size >= max_size:
            max_size = keys.size
        print('Diameter is------------------>', round(max_size)) # to  confirm the blob size detection
 
    return max_size
# ########################################################################################

def get_distance_with_cam(blob_size):
    """
    Calculate distance based on blob size
    """
    
    if blob_size > 0:
        distance = (135142.26678986842/blob_size) -114.93114618701983
        print('Distance to wall is   -----------> ', distance)
        
    else:
        distance = -1
        
        
    return distance


def slow_worker():
    """
    Slower code
    Low update rate is suitable for slow processes, such as image processing, displaying data to graph, etc;
    """
    global positions

    ret, frame = cap.read()

    # Get the blob size and convert it to distance from the wall
    keypoints = detect_blobs(frame)
    blob_size = get_blob_size(keypoints)
    positions['current_cam'] = get_distance_with_cam(blob_size)

#     print('Positions  -----> ', positions)
    image_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255),
                                             cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow("Camera image", image_with_keypoints)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        close("Image closed")


# This function will be called when CTRL+C is pressed
def signal_handler(sig, frame):
    """
    This function will be called when CTRL+C is pressed, read_sensors specific
    """
    close('\nYou pressed Ctrl+C! Closing the program nicely :)')


def close(message=""):
    """
    localization_logic specific cleanup
    """
    global running, ser, robot, timer
    print(message)
    running = False
    robot.stop()
    if ser.is_open:
        ser.close()
    timer.cancel()
    if fast_thread.is_alive:
        try:
            fast_thread.join()
        except:
            pass
    sys.exit(0)


if __name__ == "__main__":
    # Register a callback for CTRL+C
    signal.signal(signal.SIGINT, signal_handler)

    running, ser = sensors.initialize_serial('/dev/ttyUSB0')

    robot = go.EasyGoPiGo3()
    robot.set_speed(60)

    # Open the camera
    cap = cv2.VideoCapture(0)

    # Create fast_worker in a separate thread.
    fast_thread = threading.Thread(
        target=fast_worker,
        args=(running, robot, positions, ser, close)
    )
    fast_thread.daemon = True
    fast_thread.start()

    timer = RepeatTimer(0.1, slow_worker)
    timer.start()

    while running:
        time.sleep(1)
    close()
    
    
    ########################################## prep before lab
    
    ##key points backup when needed
    ''' print our x and see how to manipulate '''
#     
#      x1 = keypoints[0].pt[0]
#      x2 = keypoints[1].pt[0]
#      
#      
#     for key in keypoints:
#         x = key.pt[0]
#         y = key.pt[1]
#         s = key.size
#         print('x: ', x, 'y: ', y, 'diameter: ', s)
#              

# 
# Optimized parameters:
#   a = 135142.26678986842
#   b = -114.93114618701983