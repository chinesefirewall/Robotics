#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

video_capture_device = cv2.VideoCapture(0)

while True:
    Ret, frame = video_capture_device.read()
    cv2.imshow("Window 1", frame)

    # Quit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture_device.release()

cv2.destroyAllWindows()
