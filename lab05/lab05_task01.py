'''Niyi solomon adebayo'''

import time
import cv2
import numpy as np


# Global variable for the latest trackbar value, default is 32
trackbar_value = 71  # optimal for image 2 is around 88

# file path
file = "/home/niyi/repos/robotics-i-loti.05.010-20-21a-b88354-niyi_solomon/labs/lab05/sample01.tiff"


## -------------- detector parameters ----------------------
def blob_detector():
    blobparams = cv2.SimpleBlobDetector_Params()
    blobparams.filterByConvexity = False
    blobparams.minDistBetweenBlobs = 100
    blobparams.minArea = 500
    blobparams.filterByColor = False
    blobparams.maxArea = 200000
    blobparams.filterByInertia = False
    blobparams.filterByArea = True
    blobparams.filterByCircularity = False
    detector = cv2.SimpleBlobDetector_create(blobparams)
    return detector

detector = blob_detector()
# A callback function for a trackbar
# It is triggered every time the trackbar slider is used
def updateValue(new_value):
    # Make sure to write the new value into the global variable
    global trackbar_value
    trackbar_value = new_value

cv2.namedWindow('Thresholded_image')

# Attach a trackbar to a window named
cv2.createTrackbar("Thresholded_image", 'Thresholded_image', trackbar_value, 255, updateValue)

#Load the image from path
image = cv2.imread(file)

#Load greyscale image... 0  by default is grayscale
image_grayscale = cv2.imread(file, 0)

# infinity loop
while True:
 #Thresholding the image (Refer to opencv.org for more details)
  ret, thresh = cv2.threshold(image_grayscale, trackbar_value, 255, cv2.THRESH_BINARY)

 #gets keypoints of detections
  keypoints = detector.detect(thresh)

  #draws detected points onto the original image
  img_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

  #puts points
  #i = 0
  for i in range(len(keypoints)):
        cv2.putText(img_with_keypoints,str(int(keypoints[i].pt[0]))+" "+str(int(keypoints[i].pt[1])),(int(keypoints[i].pt[0]),int(keypoints[i].pt[1])),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

  #Display the images
  cv2.imshow('Original_grayscale', image_grayscale)
  cv2.imshow('Original_image', img_with_keypoints)
  cv2.imshow('Thresholded_image', thresh)

  # Quit the program when 'q' is pressed
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break;


# Close any windows associated with OpenCV GUI
cv2.destroyAllWindows()
print(str(keypoints))
