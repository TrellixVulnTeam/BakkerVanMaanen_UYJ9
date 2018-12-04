import numpy as np
import cv2
from collections import deque
import time
import imutils
from imutils.object_detection import non_max_suppression
from CentroidTracker import CentroidTracker

MAX_BUFFER = 16 
#   add haarcascades
full_body_cascade = cv2.CascadeClassifier('cascades/haarcascade_fullbody.xml')
upper_body_cascade = cv2.CascadeClassifier('cascades/haarcascade_upperbody.xml')
#   junk
font = cv2.FONT_HERSHEY_SIMPLEX
body_pts = deque()


def haar_detect():
    #   start video from file
    cap = cv2.VideoCapture("walking_sample4.mp4")
    start_time = time.time()
    
    while(cap.isOpened()):
        #   Capture frame-by-frame
        ret, frame = cap.read()
        #   frame width & height
        FRAME_WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        FRAME_HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #   Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #   cascades detect multiscale
        full_bodies = full_body_cascade.detectMultiScale(frame, scaleFactor=1.35, minNeighbors=4, minSize=(30,30))
        upper_bodies = upper_body_cascade.detectMultiScale(frame, scaleFactor=1.50, minNeighbors=4) 
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
            roi_gray = gray[y:y+height, x:x+width]
            roi_color = frame[y:y+height, x:x+width]
        
        if len(body_pts) > 1:
            for i in range(1, len(body_pts)):
                thickness = int(np.sqrt((i * 1.01) / float(i+1)) * 2.5)
                cv2.line(frame, body_pts[i-1], body_pts[i], (255, 0, 0), thickness)
        
        end_time = time.time()
        cv2.putText(frame, "Time Elapsed: " + str(end_time-start_time), (20, 20), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
     
        #   Display the resulting frame
        cv2.imshow('nigh7fox', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def hog_detect():
    #   initialize HOG people detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    #   deque of center pointns with a max length of buffer size
    detections = deque(maxlen=MAX_BUFFER)

    #   start video from file
    cap = cv2.VideoCapture("walking_sample8.mp4")
    
    #  counters
    right_counter = 0
    left_counter = 0
    people_in_frame_count = 0

    while(cap.isOpened()): 
        #   setup
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=min(600, frame.shape[1])) 
        orig = frame.copy() 
        (rects, weights) = hog.detectMultiScale(frame,winStride=(4,4),padding=(16,16),scale=1.05)
        
        #   frame information
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        #   lines for counting people
        cv2.line(frame, (150, 0), (150, 600), (0, 0, 255), 2)
        cv2.line(frame, (450, 0), (450, 600), (0, 0, 255), 2)
        
        #   use centroid method of uniquely identifying objects found
        ct = CentroidTracker()
        
        #   detection using hogDetectMultiScale
        for i, (x, y, w, h) in enumerate(rects):
            #   track centers of detected objects
            center = (int((x+w) - (w/2)), int((y+h) - (h/2)))
            detections.append(center)
            cv2.circle(frame, (center), 3, (0, 0, 255), 2) 
            #   contrail
            if len(detections) > 1:
                for i in range(1, len(detections)):
                    #   MAX_BUFFER = length of deque for contrail
                    #   a bigger length will have a longer tail
                    thickness = int(np.sqrt(MAX_BUFFER/float(i+1)) * 1.80)
                    #   change color on different values?
                    line_color = (255, 255, 0)
                    cv2.line(frame, detections[i-1], detections[i], line_color, thickness)
        
        #   !! NEED TO READ MORE ABOUT NON-MAXIMA-SUPPRESSION !!!
        #   apply non-maxima suppression to the bounding boxes using a
        #   fairly large overlap threshold to try to maintain overlapping
	#   boxes that are still people
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)	
        # draw the final bounding boxes, this ensures less boxes will be drawn at detection.
        for (xA, yA, xB, yB) in pick:
            #   update centroids -> centers of objects found look above for center example
            objects = ct.update(pick)
            #   center of object
            #   cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 1)
            #   loop over the tracked objects
            for (objectID, centroid) in objects.items():
                #   draw both the ID of the object and the centroid of the
		#   object on the output frame
                people_in_frame_count = len(objects)
                text = "Person {}".format(objectID)
                cv2.putText(frame,text,(centroid[0]-10,centroid[1]-10),font,0.5,(0, 0, 255),1)
        
        #   current time in video in ms (divided by 1000) for seconds
        duration = round((cap.get(cv2.CAP_PROP_POS_MSEC)/1000), 2)
        
        #   Texts
        cv2.putText(frame, "Right counter: " + str(right_counter) , (20, 40), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA) 
        cv2.putText(frame, "Left counter: " + str(left_counter), (20, 60), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA) 
        cv2.putText(frame, "Time / FPS: " + (str(duration) + " - " + str(fps)), (20, 20), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA) 
        cv2.putText(frame, "Total being detected: " + str(people_in_frame_count), (400, 20), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA) 
        
        #   Display the resulting frame
        cv2.imshow("HOG with Non Max Suppression", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


#   detection types
hog_detect()
#   haar_detect()

#   When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

