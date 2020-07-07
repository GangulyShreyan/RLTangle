import cv2
import numpy as np

def color():
    img = cv2.imread('output.jpg')
    roi = img[100:300, 0:200]
    roicvt = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    min = np.min(roicvt, axis = 1)
    actualmin = np.min(min, axis = 0)
    max = np.max(roicvt, axis = 1)
    actualmax = np.max(max, axis = 0)

    return[actualmin, actualmax]


