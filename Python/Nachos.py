import numpy as np
import cv2
from collections import deque

#   start video from file
cap = cv2.VideoCapture("walking.avi")
#   add haarcascades
full_body_cascade = cv2.CascadeClassifier('cascades/haarcascade_fullbody.xml')
upper_body_cascade = cv2.CascadeClassifier('cascades/haarcascade_upperbody.xml')
upper_body_pts = deque()


while(cap.isOpened()):
    #   Capture frame-by-frame
    ret, frame = cap.read()
    #   frame width & height
    FRAME_WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    FRAME_HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #   Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #   cascades detect multiscale
    full_bodies = full_body_cascade.detectMultiScale(frame, scaleFactor=1.25, minNeighbors=3)
    upper_bodies = upper_body_cascade.detectMultiScale(frame, scaleFactor=1.15, minNeighbors=3) 
    #   X Y grid
    cv2.line(frame, (0, 240), (640, 240), (0, 255, 0), 1) 
    cv2.line(frame, (320, 0), (320, 480), (0, 255, 0), 1)

    #   Upperbodies cascade detection
    for(x, y, width, height) in upper_bodies:
        #   put dot in the center of detected upper body
        center = (int((x+width) - (height/2)), int((y+height) - (height/2)))
        cv2.circle(frame, (center), 3, (0, 255, 0), 2) 
        upper_body_pts.append(center)
        
        roi_gray = gray[y:y+height, x:x+width]
        roi_color = frame[y:y+height, x:x+width]
    
    #   Full bodies cascade detection
    for (x, y, width, height) in full_bodies:
        cv2.rectangle(frame,(x, y),(x+width,  y+height), (0, 0, 255), 1)  
        
        roi_gray = gray[y:y+height, x:x+width]
        roi_color = frame[y:y+height, x:x+width]
    
    if len(upper_body_pts) > 1:
        for i in range(1, len(upper_body_pts)):
            thickness = 1
            cv2.line(frame, upper_body_pts[i-1], upper_body_pts[i], (255, 0, 0), thickness)


    #   Display the resulting frame
    cv2.imshow('nigh7fox', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#   When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

