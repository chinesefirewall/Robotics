'''Niyi Solomon Adebayo

'''
import numpy as np
import cv2
import time
import easygopigo3 as go

## robot driving
drive = go.EasyGoPiGo3()

# Open the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

# def default_values():
#     global hH, hS, hV, lH, lS, lV
#     file_name = open("trackbar.txt",'r')
#     obj = file_name.readline()
#     bars = obj.split(",")
#     #bars = bars.strip()
#     lH =int(bars[0])
#     hH =int(bars[1])
#     lS =int(bars[2])
#     hS =int(bars[3])
#     lV =int(bars[4])
#     hV =int(bars[5])
#     file.close()
#     return 

# global variables
image_center = 320
coord_diff = 0
middle_point = 0


def drive_forward():
    global image_center, coord_diff, middle_point
    if middle_point > image_center + 60:
        drive.spin_left()
        print('SPIN LEFT')
    elif middle_point < image_center - 60:
        drive.spin_right()
        print('SPIN RIGHT')
    else:
        drive.forward()
        print('MOVING FORWARD')
        
    if coord_diff > 330:
        drive.drive_cm(60)
        print('DRIVE 50CM ')
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
#      default_values()

    print("default value not set...manually getting values")
    # colour detection limits
    # initial limits for green pole
    lH = 0
    hH = 31
    lS = 60
    hS = 255
    lV = 0
    hV = 255

    kernel_size = 5
except:
    print('EXCEPT ERROR')
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
    blobparams.minDistBetweenBlobs = 30
    blobparams.minArea = 150
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


detector = blob_detector()
count = 0
# iscentered = False

drive.set_speed(100)
center =  0
upper_limit = 1.2 # 1.02 1.32
lower_limit = 1.02 # 1.32
while True:
    
    # Read the image from the camera
    width = 256
    height = 220
    
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
    size_list = []
#         
#     a1 = keypoints[0].size # getting size of the blob
#     a2 = keypoints[1].size
#     size_list.append(a1)
#     size_list.append(a2)
#     print('size list',size_list)
#     
#     x1 = max(size_list) # assign small value to x2 and large value to x1
#     x2 = min(size_list)
# 
#     
#     upper_limit =x1/x2
# #     lower_limit = x1/x2
#     print('upper limit is: ', upper_limit)
# #     print('lower limit is: ', lower_limit)
# #     
    ###################    MAIN DRIVING LOGIC PART  ################################
    is_centered = False
    print(' is_centered = False')
    if len(keypoints)==2:
                
        drive.set_speed(50) ##
        print('2 pillars found')
        drive.stop()
        
#         size_list = []
        
        pt1 = keypoints[0].pt[0]
        size1 = keypoints[0].size # getting size of the blob
        
        pt2 = keypoints[1].pt[0]
        size2 = keypoints[1].size
        
        if size2 > size1:
            
            holder_coord = pt1
            pt1= pt2
            pt2 = holder_coord
            
            
            holder_size = size1
            size1 = size2
            size2 = holder_size
            
        
#         size_list.append(a1)
#         size_list.append(a2)
#         
        ###############################
        x1 = pt1
        x2 = pt2
        
#         size1 = max(size_list) # assign small value to x2 and large value to x1
#         size2 = min(size_list)
        
        middle_point = (x1+x2)/2
        coord_diff = abs(x1-x2)
        print('coord difference  ',coord_diff)
        diameter_diff = size1/size2
        
        if middle_point > image_center + 10:
            
            
#             drive.drive_cm(5)
            drive.right()
            print(middle_point, 'is > ', image_center, ' SPIN RIGHT >------ ')
            
        elif middle_point < image_center - 10:
#             drive.drive_cm(5)
            drive.left() 
            print(middle_point, 'is < ', image_center, 'SPIN LEFT ------<')
            
        else:
            is_centered = True
            print('is_centered is True')
            
        if is_centered == True and  coord_diff < 400:
            diameter_diff = size1/size2
    
        ###---driving logic---#####
            if diameter_diff < upper_limit:
                
                drive.set_speed(80)
                drive_forward()
                print('     FORWARD   ')
                
            elif pt1 > pt2:
                drive.set_speed(80)
                drive.turn_degrees(-45, blocking = True)
                drive.drive_cm(30)
                drive.turn_degrees(45, blocking = True)
                drive_forward()
                print('recenter  right')
                
            
            elif pt2 > pt1:
                drive.set_speed(80)
                drive.turn_degrees(45, blocking = True)
                drive.drive_cm(30)
                drive.turn_degrees(-45, blocking = True)
                drive_forward()
                print('recenter left')
        else:
            is_centered == False
        
##########################  -------- NO BLOB DETECTED --------------###########################################
                 
    #rotates while finds two blops
    else:
        drive.set_speed(50)
        if coord_diff > 320:
            drive.drive_cm(20)
            print('DRIVE 20CM ')
            drive.stop()
        
        elif len(keypoints)==0 or len(keypoints)==1:
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




