import cv2
import numpy as np
import matplotlib.pyplot as plt

def updateKernelValue(new_value):
  # make sure to write the new value into the global variable
  global kernel_size
  kernel_size = new_value

kernel_size = 1

cv2.namedWindow('open_image')
cv2.createTrackbar("Kernel size", 'open_image', kernel_size, 30, updateKernelValue)

img = cv2.imread('/home/niyi/repos/robotics-i-loti.05.010-20-21a-b88354-niyi_solomon/labs/lab06/Task1.png')
#kernel = np.ones((5,5),np.uint8)
# erosion = cv2.erode(img,kernel,iterations = 1)
# dilation = cv2.dilate(img,kernel,iterations = 1)
while True:
    kernel = np.ones((1+2*kernel_size, 1+2*kernel_size), np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

    cv2.imshow('open_image', opening)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close any windows associated with OpenCV GUI
cv2.destroyAllWindows()


