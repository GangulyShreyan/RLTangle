import cv2
import numpy as np
import math
import imutils

class VideoCamera(object):
    def __init__(self):
       #capturing video
       self.video = cv2.VideoCapture(1)
    
    def __del__(self):
        #releasing camera
        self.video.release()

    def get_roi(self):
        _, frame = self.video.read()
        roi = frame[100:300, 0:200]

        cv2.imwrite('output.jpg', roi)

        ret, jpeg = cv2.imencode('.jpg', roi)
        return jpeg.tobytes()


    def get_frame(self, colorobj1, colorobj2):
        _, frame = self.video.read()
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
                        distance = math.sqrt((cX2 - cX1)**2 + (cY2 - cY1)**2)

                        cv2.line(frame, (cX1, cY1), (cX2, cY2), (0,255, 0))
                        cv2.putText(frame, "Angle : " + str(round(angle, 2)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
                        cv2.putText(frame, "Length : " + str(round(distance, 2)), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

                        cv2.circle(frame, (cX1, cY1), 5, (0,0,255), 10)
                        cv2.circle(frame, (cX2, cY2), 5, (0,0,255), 10)
            

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
   