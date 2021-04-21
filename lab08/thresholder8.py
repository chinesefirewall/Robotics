'''
Niyi Solomon Adebayo

'''

import numpy as np
import cv2
import time
import math

cap = cv2.VideoCapture(0)

#user defined function that loads in pre-defined values from a text file
def getValues():

    global hH, hS, hV, lH, lS, lV
    file = open("trackbar_defaults.txt","r")
    line = file.readline()
    values = line.split(" ")
    #values.strip()
    lH =int(values[0])
    hH =int(values[1])
    lS =int(values[2])
    hS =int(values[3])
    lV =int(values[4])
    hV =int(values[5])
    file.close()
    return

# A callback function for each trackbar parameter
# write the new value into the global variable everytime
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

#Another safety net to access default value.txt file... otherwise it continues
try:
    getValues()
except:
    print("values txt file not acquired, setting default values")
    # colour detection limits
    lH = 94
    lS = 255
    lV = 168
    hH = 255
    hS = 83
    hV = 256

# --------------------- create track bar for each param --------------------------

cv2.namedWindow('Processed')
cv2.createTrackbar("Low H", 'Processed', lH, 255, updatelH)
cv2.createTrackbar("High H", 'Processed', hH, 255, updatehH)
cv2.createTrackbar("Low S", 'Processed', lS, 255, updatelS)
cv2.createTrackbar("High S", 'Processed', hS, 255, updatehS)
cv2.createTrackbar("Low V", 'Processed', lV, 255, updatelV)
cv2.createTrackbar("High V", 'Processed', hV, 255, updatehV)

## -------------- detector parameters ----------------------
def blob_detector():

    blobparams = cv2.SimpleBlobDetector_Params()
    blobparams.filterByConvexity = False
    blobparams.minDistBetweenBlobs = 1000
    blobparams.minArea = 1000
    blobparams.filterByColor = False
    blobparams.maxArea = 200000000
    blobparams.filterByInertia = False
    blobparams.filterByArea = True
    blobparams.filterByCircularity = False

    detector = cv2.SimpleBlobDetector_create(blobparams)
    return detector

#detector = initdetector()
# Read the time before frame
start_time = time.time()


'''
Processing time for this frame = Current time – time when previous frame processed
So fps at the current moment will be :
FPS = 1/ (Processing time for this frame)
 source: https://www.geeksforgeeks.org/python-displaying-real-time-fps-at-which-webcam-video-file-is-processed-using-opencv/

'''
max_size = 0
while True:

  
  #read the image from the camera
  ret, frame = cap.read()

  # You will need this later
  # frame = cv2.cvtColor(frame, ENTER_CORRECT_CONSTANT_HERE)

  lowerThresh = np.array([lH, lS, lV])
  upperThresh = np.array([hH, hS, hV])

  # Our operations on the frame come here
  HSV_img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
  thresholded_img = cv2.inRange(HSV_img, lowerThresh, upperThresh)
  thresholded_img = 255 - thresholded_img
  thresholded_img = cv2.rectangle(thresholded_img, (1,1), (frame.shape[1]-1,frame.shape[0]-1), (1,1,1),3)

  detector = blob_detector()
  keypoints = detector.detect(thresholded_img)
  
  for keys in keypoints:
      if keys.size >= max_size:
          max_size = keys.size
          print('Diameter is------------------>', round(max_size)) # to  confirm the blob size detection

  # puts points
  for i in range(len(keypoints)):
      cv2.putText(frame, str(int(keypoints[i].pt[0])) + " " + str(int(keypoints[i].pt[1])),
                  (int(keypoints[i].pt[0]), int(keypoints[i].pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)

# performs masking on an original image, original image gets original image value if mask is 255
    # outimage = cv2.bitwise_and(frame, frame, mask = thresholded)
  current_time = time.time()
  diff = (current_time - start_time)
  start_time = current_time

  # Write some text onto the frame (FPS number)
  cv2.putText(frame, str(np.floor(1 / diff)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

  # puts detected points on original image
  img_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255),
                                         cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

  # Display the resulting frame
  cv2.imshow('Processed', thresholded_img)
  cv2.imshow('Original', img_with_keypoints)

  # Quit the program when 'q' is pressed
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# When everything done, release the capture, and now save the  new thresholding values used
print('closing program')
cap.release()
cv2.destroyAllWindows()
file = open("trackbar_defaults.txt","w+")
file.write(str(lH)+str(" ")+str(hH)+str(" ")+str(lS)+str(" ")+str(hS)+str(" ")+str(lV)+str(" ")+str(hV))
file.close()


