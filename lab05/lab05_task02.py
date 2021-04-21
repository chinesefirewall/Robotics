'''Niyi Solomon Adebayo'''
'''BACKGROUND

In OpenCV finding the frame rate of a connected camera / webcam is not straight forward. 
The documentation says that get(CAP_PROP_FPS) or get(CV_CAP_PROP_FPS) gives the frames per second. 
Now that is true for video files, but not for webcams. For webcams and many other connected cameras, 
you have to calculate the frames per second manually. 
You can read a certain number of frames from the video and see how much time has elapsed to calculate frames per second.
SOURCE: https://www.learnopencv.com/how-to-find-frame-rate-or-frames-per-second-fps-in-opencv-python-cpp/
'''

import cv2
import numpy as np
import time

# Open the camera
cap = cv2.VideoCapture(0)

#current time of capture
start_time = time.time()

'''
Processing time for this frame = Current time – time when previous frame processed
So fps at the current moment will be :
FPS = 1/ (Processing time for this frame)
 source: https://www.geeksforgeeks.org/python-displaying-real-time-fps-at-which-webcam-video-file-is-processed-using-opencv/

'''
while True:
    # Read the image from the camera
    ret, frame = cap.read()
    #frame = cv2.flip(frame, frame, 0)
    current_time = time.time()
    difference = (current_time - start_time)
    start_time = current_time


    # Write fps onto the frame in real time
    cv2.putText(frame, str(np.floor(1/difference)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 1000), 2)

    # Show this image on a window named "Original"
    cv2.imshow('Original', frame)

    # Quit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('a'):
        break
# When everything done, release the capture
print('closing program')
cap.release()
cv2.destroyAllWindows()

