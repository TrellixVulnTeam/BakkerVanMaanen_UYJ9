import numpy as np
import cv2
from collections import deque
import time
import imutils
from imutils.object_detection import non_max_suppression
from CentroidTracker import CentroidTracker


#   add haarcascades
upper_body_cascade = cv2.CascadeClassifier('cascades/haarcascade_upperbody.xml')
lower_body_cascade = cv2.CascadeClassifier('cascades/haarcascade_lowerbody.xml')

#   junk
font = cv2.FONT_HERSHEY_SIMPLEX
MAX_BUFFER = 16

def haar_detect():
    #   start video from file
    cap = cv2.VideoCapture("walking_sample7.mp4")
    start_time = time.time()
    body_pts = deque(maxlen=MAX_BUFFER)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    #  counters
    right_counter = 0
    left_counter = 0
    people_in_frame_count = 0

    while(cap.isOpened()):
        #   Capture frame-by-frame
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=min(600, frame.shape[1]))

        #   Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #   load detect multiscale to detect
        #   upper_bodies = upper_body_cascade.detectMultiScale(frame, scaleFactor=1.30, minNeighbors=5)
        lower_bodies = lower_body_cascade.detectMultiScale(frame, scaleFactor=1.25, minNeighbors=5)

        #   left n right lines
        cv2.line(frame, (500, 0), (500, 600), (0, 255, 0), 1)
        cv2.line(frame, (100, 0), (100, 600), (0, 255, 0), 1)

        #   Upperbodies cascade detection
        for(x, y, width, height) in lower_bodies:
            roi_gray = gray[y:y+height, x:x+width]
            roi_color = frame[y:y+height, x:x+width]
            center = (int((x+width) - (width/2)), int((y+height) - (height/2)))
            body_pts.append(center)
            cv2.circle(frame, center, 5, (0, 0, 255), 2)
            #   contrail
            if len(body_pts) > 1:
                for i in range(1, len(body_pts)):
                    thickness = int(np.sqrt(MAX_BUFFER / float(i+1)) * 2.50)
                    cv2.line(frame, body_pts[i-1], body_pts[i], (255, 255, 0), thickness)

        #   current time in video in ms (divided by 1000) for seconds
        duration = round((cap.get(cv2.CAP_PROP_POS_MSEC)/1000), 2)

        #   Texts
        cv2.putText(frame, "Right counter: " + str(right_counter) , (20, 40), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, "Left counter: " + str(left_counter), (20, 60), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, "Time / FPS: " + (str(duration) + " - " + str(fps)), (20, 20), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, "Total being detected: " + str(people_in_frame_count), (400, 20), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

        #   Display the resulting frame
        cv2.imshow('Haar Cascade Detection', frame)
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
        (rects, weights) = hog.detectMultiScale(frame,winStride=(5,5),padding=(8,8),scale=1.15)

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
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.85)
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
#   hog_detect()
haar_detect()

#   When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

