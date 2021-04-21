'''Niyi Solomon Adebayo

'''

import numpy as np
import cv2
import time
import easygopigo3 as go
#from easygopigo3 import EasyGoPiGo3 as go

## robot driving
drive = go.EasyGoPiGo3()




# Open the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

def default_values():
    global hH, hS, hV, lH, lS, lV
    file_name = open("trackbar.txt",'r')
    obj = file_name.readline()
    bars = obj.split(",")
    #bars = bars.strip()
    lH =int(bars[0])
    hH =int(bars[1])
    lS =int(bars[2])
    hS =int(bars[3])
    lV =int(bars[4])
    hV =int(bars[5])
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

def updateKernelValue(new_value):
  global kernel_size
  kernel_size = new_value
#write the new value into the global variable



######################


try:
     default_values()
except:
    print("default value not set...manually getting values")
    # colour detection limits
    # initial limits
    lH = 0
    hH = 162
    lS = 50
    hS = 233
    lV = 193
    hV = 255

kernel_size = 5

##################


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

detector = blob_detector()
while True:
    
    # Read the image from the camera
    width = 256
    height = 120
    
    for i in range(3):
        
        ret, video = cap.read()
    video = video[height:width]
    print('video ', len(video[0]))
    # median blur
    #frame_blurred = cv2.medianBlur(video,1+2*kernel_size)

    # gaussian
    # frame_blurred = cv2.GaussianBlur(video, (1 + 2 * kernel_size, 1 + 2 * kernel_size), 0)

    # You will need this later
    # frame = cv2.cvtColor(frame, ENTER_CORRECT_CONSTANT_HERE)

    lowerThresh = np.array([lH, lS, lV])
    upperThresh = np.array([hH, hS, hV])
    
    
    thresholded = cv2.inRange(video, lowerThresh, upperThresh)
    a = thresholded.shape # to get fram height and width
    f_width = a[1]
    f_height = a[0]
    print('frame height is ', a[0], '  and frame width s ', a[1])
    #thresholded = cv2.dilate(thresholded, iterations = 1 )
    thresholded = cv2.rectangle(thresholded, (0,0), (f_width-1, f_height-1),(255),2)
#    thresholded = cv2.inRange(frame_blurred , lowerThresh, upperThresh)
    thresholded_img = 255 - thresholded
    #thresholded_img = thresholded
#     outimage = cv2.bitwise_and(video, video, mask=thresholded)

    
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
    
    ######################
#     for key in keypoints:
#         x1 = key.pt[0]
#         x2 = key.pt[1]
#         s = key.size
#         print('x1: ', x1, 'x2: ', x2, 'diameter: ', s)
#              
#####################

    middle_number_allowance1 = 270
    middle_number_allowance2 = 370
    try:
            
        ### robot control
        drive.set_speed(50)
        print('length of key point: ',len(keypoints))
        x1 = keypoints[0].pt[0]
        x2 = keypoints[0].pt[1]
        print('x1: ', x1, 'x2: ', x2)
        
        if x1 > middle_number_allowance1 and x1 < middle_number_allowance2:
            print("it is in center ")# do nothing
            drive.stop()
            
        elif x1 < middle_number_allowance1:  
            print('spin left')
            drive.spin_left()
        
        elif x1 > middle_number_allowance2:
            drive.spin_right()
            print('spin right')
    except:
        print('No keypoints detected')

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
file = open("trackbar.txt","w+")
file.write(str(lH)+str(",")+str(hH)+str(",")+str(lS)+str(",")+str(hS)+str(",")+str(lV)+str(",")+str(hV))
file.close()


###########################

# x = 130 to 370
# y = 32 to 42





