'''Niyi Solomon Adebayo

'''

import numpy as np
import cv2
import time
from easygopigo3 import EasyGoPiGo3 # importing the EasyGoPiGo3 class

## robot driving
drive = go.EasyGoPiGo3()


# Open the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

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

def updateKernelValue(new_value):
  global kernel_size
  kernel_size = new_value
#write the new value into the global variable


# initial limits
lH = 0
hH = 173
lS = 50
hS = 233
lV = 193
hV = 255
kernel_size = 15




# --------------------- create track bar for each param --------------------------

cv2.namedWindow('Processed')
cv2.createTrackbar("Low H", 'Processed', lH, 255, updatelH)
cv2.createTrackbar("High H", 'Processed', hH, 255, updatehH)
cv2.createTrackbar("Low S", 'Processed', lS, 255, updatelS)
cv2.createTrackbar("High S", 'Processed', hS, 255, updatehS)
cv2.createTrackbar("Low V", 'Processed', lV, 255, updatelV)
cv2.createTrackbar("High V", 'Processed', hV, 255, updatehV)
cv2.createTrackbar("Kernel size", 'Processed', kernel_size, 100, updateKernelValue)

## -------------- detector parameters ----------------------
def blob_detector():

    blobparams = cv2.SimpleBlobDetector_Params()
    blobparams.filterByConvexity = False
    blobparams.minDistBetweenBlobs = 2000
    blobparams.minArea = 200
    blobparams.filterByColor = True
    blobparams.maxArea = 30000
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


while True:
    # Read the image from the camera
    ret, video = cap.read()
    video = video[180:256]
    # median blur
    #frame_blurred = cv2.medianBlur(video,1+2*kernel_size)

    # gaussian
    # frame_blurred = cv2.GaussianBlur(video, (1 + 2 * kernel_size, 1 + 2 * kernel_size), 0)

    # You will need this later
    # frame = cv2.cvtColor(frame, ENTER_CORRECT_CONSTANT_HERE)

    lowerThresh = np.array([lH, lS, lV])
    upperThresh = np.array([hH, hS, hV])
    
    thresholded = cv2.inRange(video, lowerThresh, upperThresh)
#     thresholded = cv2.rectangle(thresholded, (0,0), (width-1, height-1),(255,255,255),2)
#    thresholded = cv2.inRange(frame_blurred , lowerThresh, upperThresh)
    thresholded_img = 255 - thresholded
    #thresholded_img = thresholded
#     outimage = cv2.bitwise_and(video, video, mask=thresholded)

    detector = blob_detector()
    keypoints = detector.detect(thresholded_img)
    i=0
    # puts points
    for i in range(len(keypoints)):
        cv2.putText(thresholded_img, str(int(keypoints[i].pt[0])) + " " + str(int(keypoints[i].pt[1])),
                    (int(keypoints[i].pt[0]), int(keypoints[i].pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)
        
#         cv2.putText(video, str(int(keypoints[i].pt[0])) + " " + str(int(keypoints[i].pt[1])),
#                     (int(keypoints[i].pt[0]), int(keypoints[i].pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)

    # performs masking on an original image, original image gets original image value if mask is 255
    # outimage = cv2.bitwise_and(frame, frame, mask = thresholded)
    current_time = time.time()
    diff = (current_time - start_time)
    start_time = current_time

    # Write some text onto the frame (FPS number)
    #cv2.putText(video, str(np.floor(1 / diff)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(thresholded_img, str(np.floor(1 / diff)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    

    # puts detected points on original image
    img_with_keypoints = cv2.drawKeypoints(video, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    ###################### there will be 2 x and 2 y, so i need to work only witht the Xs.
    ''' print our x and see how to manipulate '''
    
     x1 = keypoints[0].pt[0]
     x2 = keypoints[1].pt[0]
     
     
    for key in keypoints:
        x = key.pt[0]
        y = key.pt[1]
        s = key.size
        print('x: ', x, 'y: ', y, 'diameter: ', s)
             
      #####################
    	# x = 130 to 370
	# y = 32 to 42
    middle_number_allowance1 = value of x - allowance
    middle_number_allowance2 = value of x + allowance
	
	### robot control
	#drive.set_speed(100)
	if x > middle_number_allowance1 and x < middle_number_allowance2:
		print("it is in center ")# do nothing
		
	elif x < middle_number_allowance1:	
		drive.spin_left()
	
	elif x > middle_number_allowance2:
		drive.spin_right()


    
    
    
    # Display the resulting frame
    cv2.imshow('Original vid', img_with_keypoints)
    cv2.imshow('Thresh vid', thresholded_img)
    #cv2.imshow('Blurred vid', frame_blurred)
    # Quit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
# When everything done, release the capture
print('closing program')
cap.release()
cv2.destroyAllWindows()



###########################

# x = 130 to 370
# y = 32 to 42





