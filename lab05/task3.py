'''Niyi Solomon Adebayo

'''

import numpy as np
import cv2
import time

# Open the camera
cap = cv2.VideoCapture(0)

# A callback function for each trackbar parameter
# write the new value into the global variable everytime
def updatelR(new_value):
  global hB, hG, hR, lB, lG, lR
  lR = new_value
  return

def updatehR(new_value):
  global hB, hG, hR, lB, lG, lR
  hR = new_value
  return

def updatelB(new_value):
  global hB, hG, hR, lB, lG, lR
  lB = new_value
  return

def updatehB(new_value):
  global hB, hG, hR, lB, lG, lR
  hB = new_value
  return


def updatelG(new_value):
  global hB, hG, hR, lB, lG, lR
  lG = new_value
  return


def updatehG(new_value):
  global hB, hG, hR, lB, lG, lR
  hG = new_value
  return
# ------------------------------------------

# initial limits
lB = 0
lG = 40
lR = 125
hB = 10
hG = 80
hR = 255

# --------------------- create track bar for each param --------------------------

cv2.namedWindow('Processed')
cv2.createTrackbar("Low Green", 'Processed', lG, 255, updatelG)
cv2.createTrackbar("High Green", 'Processed', hG, 255, updatehG)
cv2.createTrackbar("Low Red", 'Processed', lR, 255, updatelR)
cv2.createTrackbar("High Red", 'Processed', hR, 255, updatehR)
cv2.createTrackbar("Low Blue", 'Processed', lB, 255, updatelB)
cv2.createTrackbar("High Blue", 'Processed', hB, 255, updatehB)

## -------------- detector parameters ----------------------
def blob_detector():

    blobparams = cv2.SimpleBlobDetector_Params()
    blobparams.filterByConvexity = False
    blobparams.minDistBetweenBlobs = 200
    blobparams.minArea = 900
    blobparams.filterByColor = False
    blobparams.maxArea = 20000
    blobparams.filterByInertia = False
    blobparams.filterByArea = True
    blobparams.filterByCircularity = False
    detector = cv2.SimpleBlobDetector_create(blobparams)
    return detector


#current time of capture
start_time = time.time()

'''
Processing time for this frame = Current time – time when previous frame processed
So fps at the current moment will be :
FPS = 1/ (Processing time for this frame)
 source: https://www.geeksforgeeks.org/python-displaying-real-time-fps-at-which-webcam-video-file-is-processed-using-opencv/

'''
max_size = 0
while True:
    # Read the image from the camera
    ret, video = cap.read()

    # You will need this later
    #video  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    lowerThresh = np.array([lB, lG, lR])
    upperThresh = np.array([hB, hG, hR])

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
    thresholded = cv2.inRange(video, lowerThresh, upperThresh)
    thresholded2 = 255 - thresholded
    outimage  = cv2.bitwise_and(video, video, mask=thresholded)

    detector = blob_detector()
    keypoints = detector.detect(thresholded2)
    
        
    """Find the size of biggest keypoint    """
    
    for keys in keypoints:
        if keys.size >= max_size:
            max_size = keys.size
        print('Diameter is------------------>', round(max_size)) # to  confirm the blob size detection


    # puts points
    for i in range(len(keypoints)):
        cv2.putText(video, str(int(keypoints[i].pt[0])) + " " + str(int(keypoints[i].pt[1])),
                    (int(keypoints[i].pt[0]), int(keypoints[i].pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)

    # performs masking on an original image, original image gets original image value if mask is 255
    # outimage = cv2.bitwise_and(frame, frame, mask = thresholded)
    current_time = time.time()
    diff = (current_time - start_time)
    start_time = current_time

    # Write some text onto the frame (FPS number)
    cv2.putText(video, str(np.floor(1 / diff)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # puts detected points on original image
    img_with_keypoints = cv2.drawKeypoints(video, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Display the resulting frame
    cv2.imshow('Original vid',  img_with_keypoints)
    cv2.imshow('Processed vid', outimage)
    cv2.imshow('Processed vid2', thresholded)
    # Quit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
print('closing program')
cap.release()
cv2.destroyAllWindows()
