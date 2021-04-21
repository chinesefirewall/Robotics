#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file imports your code from localization_logic.py and uses class Visualisation from visualisation.py.
You can change the code at your own risk!
"""

import easygopigo3 as go
import signal
import pyqtgraph as pg
import cv2
import threading
import visualisation
import read_sensors as sensors
import localization_logic as loc
import sys

# Dictionary for holding positions
positions = {'current_marker': 0, 'current_us': -1, 'current_enc': -1, 'current_cam': -1}


def slow_worker():
    """
    Slower code
    Low update rate is suitable for slow processes, such as image processing, displaying data to graph, etc;
    """
    global positions

    ret, frame = cap.read()
    # Get the blob size and convert it to distance from the wall
    keypoints = loc.detect_blobs(frame)
    blob_size = loc.get_blob_size(keypoints)
    positions['current_cam'] = loc.get_distance_with_cam(blob_size)

    visual.draw(positions['current_us'], positions['current_enc'], positions['current_cam'])


def signal_handler(sig, frame):
    """
    This function will be called when CTRL+C is pressed
    """
    close('\nYou pressed Ctrl+C! Closing the program nicely :)')


def close(message=""):
    """
    localization_gui specific cleanup function
    """
    global running, ser, robot, timer
    print(message)
    running = False
    robot.stop()
    if ser.is_open:
        ser.close()
    timer.stop()
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

    # Create timer
    timer = pg.QtCore.QTimer()

    # Initialize visualization logic
    visual = visualisation.Visualisation()
    visual.set_on_close_function(close, "Plotter window closed.")

    # Create fast_worker in a separate thread
    fast_thread = threading.Thread(
        target=loc.fast_worker,
        args=(running,
        robot,
        positions,
        ser,
        close)
    )
    fast_thread.daemon = True
    fast_thread.start()

    # Connecting slow_worker to timer, it will be executed with certain interval
    timer.timeout.connect(slow_worker)

    # Start timer with interval 100 msec
    timer.start(100)

    # Start the visualisation app
    visual.run()
    close()
