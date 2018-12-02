import numpy as np
import cv2

cap = cv2.VideoCapture("walking.avi")
fullBodyCascade = cv2.CascadeClassifier('cascades/haarcascade_fullbody.xml')
while(cap.isOpened()):
    #   Capture frame-by-frame
    ret, frame = cap.read()
    FRAME_WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    FRAME_HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #   Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #   Cascades
    bodies = fullBodyCascade.detectMultiScale(frame, scaleFactor=1.15, minNeighbors=3, minSize=(20, 20))
    for (x, y, width, height) in bodies:
        cv2.rectangle(frame,(x, y),(x + width,  y + height), (0 , 255, 0), 1)
        #   ROI = Region of Interest, aldus waar de object zich nu bevind
        roi_gray = gray[y:y+height, x:x+width]
        roi_color = frame[y:y+height, x:x+width]   
    #   Display the resulting frame
    cv2.imshow('bitch', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#   When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
