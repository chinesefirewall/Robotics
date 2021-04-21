'''Niyi Solomon Adebayo

'''
import numpy as np
import cv2
import time
import easygopigo3 as go
#from easygopigo3 import EasyGoPiGo3 as go

## robot driving
drive = go.EasyGoPiGo3()

# global variables
center_image = 320
coord_difference = 0
middle_point = 0

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


def drive_forward():
    global image_center, coord_difference, middle_point
    if middle_point > image_center + 100:
        drive.spin_left()
    elif middle_point < image_center - 100:
        drive.spin_right()
    else:
        drive.forward()
        print('MOVING FORWARD')
        
    if coord_diff >580:
        drive_cm(50)
        drive.stop()

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


try:
     default_values()
except:
    print("default value not set...manually getting values")
    # colour detection limits
    # initial limits for green pole
    lH = 0
    hH = 45
    lS = 47
    hS = 84
    lV = 97
    hV = 255

kernel_size = 5

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
    blobparams.minDistBetweenBlobs = 5
    blobparams.minArea = 100
    blobparams.filterByColor = True
    blobparams.maxArea = 10000
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

# def center_calibration(video, key):
#     
#     global count
#     det_1 = key[0].pt[0]
#     det_2 = key[1].pt[0]
#     
#     # assigning one pole to and the other to left
#     if det_1 > det_2:
#         variable_holder = det_1
#         det_1 = det_2
#         det_2 = variable_holder
#         
#     width = int((det_1 - det_2)/2)
#     center_of_pole = det_1 + width
#     allignment = 320 - center_of_pole
#     if (-5 < allignment > 5):
#         count += 1
#     
#     if allignment > 5:
#         drive.steer(3,10)
#         print("---Left---")
#         count += 1
#     
#     else:
#         print('----Right----')
#         drive.steer(10,3)
#         
#     return
# 


detector = blob_detector()
count = 0
motion = False

drive.set_speed(100)
center =  0
while True:
    
    # Read the image from the camera
    width = 256
    height = 180
    
    for i in range(3):
        
        ret, video = cap.read()
    video = video[height:width]
#     print('video ------ ', len(video[0]))
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
#     print('frame height is ', a[0], '  and frame width s ', a[1])
    thresholded = cv2.rectangle(thresholded, (0,0), (f_width-1, f_height-1),(0),2)

    thresholded_img = 255 - thresholded
#     thresholded_img = thresholded
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
    cv2.putText(video, str(np.floor(1 / diff)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#     cv2.putText(thresholded_img, str(np.floor(1 / diff)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    

    # puts detected points on original image
    img_with_keypoints = cv2.drawKeypoints(video, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


###############  check for upper and lower limits  BEFORE IMPLEMENTING ###############################
#     size_list = []
#         
#     a1 = keypoints[0].size[0] # getting size of the blob
#     a2 = keypoints[0].size[1]
#     size_list.append(a1)
#     size_list.append(a2)
#     
#     x1 = max(size_list) # assign small value to x2 and large value to x1
#     x2 = min(size_list)
# 
#     
#     upper_limit =x1/x2
#     lower_limit = x1/x2
#     print('upper limit is: ', upper_limit)
#     print('lower limit is: ', lower_limit)
    
    ###################    MAIN DRIVING LOGIC PART  ################################
    is_centered = False
    print('is_centered = False')
    if len(keypoints)==2:
        
'''        
        drive.set_speed(50) ##
        print('2 pillars found')
        drive.stop()
        
        size_list = []
        
        a1 = keypoints[0].size[0] # getting size of the blob
        a2 = keypoints[0].size[1]
        size_list.append(a1)
        size_list.append(a2)
        
        x1 = max(size_list) # assign small value to x2 and large value to x1
        x2 = min(size_list)
        middle_point = (x1+x2)/2
        coord_diff = abs(x1-x2)
        
        if middle point > image_center + 100:
            
            drive.spin_left()
            
        elif middle point < image_center - 100:
            drive.spin_right()
            
        else:
            is_centered = True
            print('is_centered is True')
            diameter_diff = x1/x2
            
        ###---driving logic---#####
            
            
        if upper_limit > diameter_diff and upper_limit < diameter_diff:
            drive.set_speed(50)
            drive.drive_forward()
        elif diameter_diff < lower_limit:
            drive.set_speed(50)
            drive.turn_degree(-45, blocking = True)
            drive.drive_cm(60)
            turn_degree(45, blocking = True)
            drive.drive_forward()
            
        
        elif diameter_diff > upper_limit:
            drive.set_speed(50)
            drive.turn_degree(45, blocking = True)
            drive.drive_cm(60)
            turn_degree(45, blocking = True)
            drive.drive_forward()
            
'''            
    
##########################  -------- NO BLOB DETECTED --------------###########################################
                 
    #rotates while finds two blops
    else:
        drive.set_speed(100)
        len(keypoints)==0 or len(keypoints)==1:
        print("NO BLOB DETECTED")
        drive.steer(-3,3)
    


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
print('write successful...')




