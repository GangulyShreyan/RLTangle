import cv2
import numpy as np
import math
import imutils
import colorpicker


colorobj1 = colorpicker.color()
colorobj2 = colorpicker.color()
cap = cv2.VideoCapture(1)

while True:
    _, frame = cap.read()
    framecvt = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    obj1 = cv2.inRange(framecvt, colorobj1[0], colorobj1[1]) 
    obj2 = cv2.inRange(framecvt, colorobj2[0], colorobj2[1])

    cnts1 = cv2.findContours(obj1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts1 = imutils.grab_contours(cnts1)
    cnts1 = sorted(cnts1, key = cv2.contourArea, reverse = True)[:10]

    cnts2 = cv2.findContours(obj2.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts2 = imutils.grab_contours(cnts2)
    cnts2 = sorted(cnts2, key = cv2.contourArea, reverse = True)[:10]

    mask1 =cv2.bitwise_and(frame, frame, mask = obj1)
    mask2 =cv2.bitwise_and(frame, frame, mask = obj2)

    mask3 = cv2.bitwise_or(mask1, mask2)

    if len(cnts1)!= 0 and len(cnts2)!= 0:
        M1 = cv2.moments(cnts1[0])
        M2 = cv2.moments(cnts2[0])
        if(M1["m00"] != 0) and (M2["m00"] != 0):
            cX1 = int(M1["m10"] / M1["m00"])    
            cY1 = int(M1["m01"] / M1["m00"])

            cX2 = int(M2["m10"] / M2["m00"])
            cY2 = int(M2["m01"] / M2["m00"])

            if(cX2 - cX1 != 0):
                angle = math.degrees(np.arctan((cY2 - cY1)/(cX2 - cX1)))

                cv2.line(frame, (cX1, cY1), (cX2, cY2), (0,255, 0))
                cv2.putText(frame, "Angle : " + str(round(angle, 2)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

                cv2.line(mask3, (cX1, cY1), (cX2, cY2), (0,255, 0))
                cv2.putText(mask3, "Angle : " + str(round(angle, 2)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

                cv2.circle(frame, (cX1, cY1), 5, (0,0,255), 10)
                cv2.circle(frame, (cX2, cY2), 5, (0,0,255), 10)

            if(cX2 - cX1 == 0):
                    angle = 90
                    
                    cv2.line(frame, (cX1, cY1), (cX2, cY2), (0,255, 0))
                    cv2.putText(frame, "Angle : " + str(round(angle, 2)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

                    cv2.line(mask3, (cX1, cY1), (cX2, cY2), (0,255, 0))
                    cv2.putText(mask3, "Angle : " + str(round(angle, 2)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

                    cv2.circle(frame, (cX1, cY1), 5, (0,0,255), 10)
                    cv2.circle(frame, (cX2, cY2), 5, (0,0,255), 10)

    cv2.imshow('mask3', mask3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
            

   