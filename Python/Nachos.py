import numpy as np
import cv2
from collections import deque

#   start video from file
cap = cv2.VideoCapture("walking_sample4.mp4")
#   add haarcascades
full_body_cascade = cv2.CascadeClassifier('cascades/haarcascade_fullbody.xml')
upper_body_cascade = cv2.CascadeClassifier('cascades/haarcascade_upperbody.xml')
body_pts = deque()
font = cv2.FONT_HERSHEY_SIMPLEX

while(cap.isOpened()):
    #   Capture frame-by-frame
    ret, frame = cap.read()
    #   frame width & height
    FRAME_WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    FRAME_HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #   Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #   cascades detect multiscale
    full_bodies = full_body_cascade.detectMultiScale(frame, scaleFactor=1.25, minNeighbors=5, minSize=(40,40))
    upper_bodies = upper_body_cascade.detectMultiScale(frame, scaleFactor=1.50, minNeighbors=3) 
    #   X Y grid
    cv2.line(frame, (0, 240), (640, 240), (0, 255, 0), 1) 
    cv2.line(frame, (320, 0), (320, 480), (0, 255, 0), 1)

    #   Upperbodies cascade detection
    for(x, y, width, height) in upper_bodies:
        cv2.rectangle(frame,(x, y),(x+width,  y+height), (255, 0, 0), 2)  
        roi_gray = gray[y:y+height, x:x+width]
        roi_color = frame[y:y+height, x:x+width]
    
    #   Full bodies cascade detection
    for (x, y, width, height) in full_bodies:
        center = (int((x+width) - (width/2)), int((y+height) - (height/2))) 
        body_pts.append(center)
        cv2.circle(frame, (center), 3, (0, 255, 0), 2) 
        cv2.rectangle(frame,(x, y),(x+width,  y+height), (0, 0, 255), 2)  
        cv2.putText(frame, 'Human', (x, y), font, 0.3, (255, 255, 255), 1, cv2.LINE_AA)
        roi_gray = gray[y:y+height, x:x+width]
        roi_color = frame[y:y+height, x:x+width]
    
    if len(body_pts) > 1:
        for i in range(1, len(body_pts)):
            thickness = int(np.sqrt((i * 1.01) / float(i+1)) * 2.5)
            cv2.line(frame, body_pts[i-1], body_pts[i], (255, 0, 0), thickness)

    #   Display the resulting frame
    cv2.imshow('nigh7fox', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#   When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

