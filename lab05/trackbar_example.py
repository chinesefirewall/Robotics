#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

# Global variable for the latest trackbar value, default is 32
trackbar_value = 32

# Open the default video camera
video_capture_device = cv2.VideoCapture(0)

# A callback function for a trackbar
# It is triggered every time the trackbar slider is used
def updateValue(new_value):
    # Make sure to write the new value into the global variable
    global trackbar_value
    trackbar_value = new_value

# Create a named window and name it 'Output'
cv2.namedWindow("Output")

# Attach a trackbar to a window named 'Output'
cv2.createTrackbar("Example trackbar", "Output", trackbar_value, 96, updateValue)

# An infinite while-loop
while True:
    # Read a single frame from the capture device (i.e. the camera)
    Ret, frame = video_capture_device.read()
    # Add the trackbar value as text on the read frame
    cv2.putText(frame, str(trackbar_value), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    # Display the frame in the window named 'Output'
    cv2.imshow("Output", frame)

    # Quit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the video capturing device
video_capture_device.release()

# Close any windows associated with OpenCV GUI
cv2.destroyAllWindows()

