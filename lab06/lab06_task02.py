

import cv2
import numpy as np
import matplotlib.pyplot as plt

def updateKernelValue(new_value):
  # make sure to write the new value into the global variable
  global kernel_size
  kernel_size = new_value

kernel_size = 1

cv2.namedWindow('closed_image')
cv2.createTrackbar("Kernel size", 'closed_image', kernel_size, 30, updateKernelValue)

img = cv2.imread('/home/niyi/repos/robotics-i-loti.05.010-20-21a-b88354-niyi_solomon/labs/lab06/Task2.png')

# image closing is dilate followed by erosion


while True:
    kernel = np.ones((1+2*kernel_size, 1+2*kernel_size), np.uint8)
    dilation = cv2.dilate(img, kernel, iterations=3)
    #closing = cv2.erode(dilation, kernel, iterations=1)

    cv2.imshow('closed_image', dilation)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close any windows associated with OpenCV GUI
cv2.destroyAllWindows()



