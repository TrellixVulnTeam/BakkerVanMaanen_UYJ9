import numpy as np
import cv2
from collections import deque
import time
import imutils
from imutils.object_detection import non_max_suppression
from CentroidTracker import CentroidTracker
from TrackableObject import TrackableObject


#   add haarcascades
smile_cascade = cv2.CascadeClassifier('cascades/haarcascade_smile.xml')

#   junk
font = cv2.FONT_HERSHEY_SIMPLEX
MAX_BUFFER = 16

def detect_smile():
    img = cv2.imread("smiling_sample3.jpg")
    frame = imutils.resize(img, width=min(600, img.shape[1]))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    smiles = smile_cascade.detectMultiScale(frame, scaleFactor=1.95)
    for(x, y, w, h) in smiles:
        cv2.rectangle(frame, (x, y), ((x+w), (y+h)), (0, 255, 0), 2)
    if smiles is None:
        return 0
    cv2.imshow("blah", frame)
    cv2.waitKey(0)


def detect_people():
    #   initialize HOG people detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    #   deque of center pointns with a max length of buffer size
    detections = deque(maxlen=MAX_BUFFER)
    trackableObjects = {}
    #   start video from file
    cap = cv2.VideoCapture("walking_sample10.mp4")
    #  counters
    right_counter = 0
    left_counter = 0
    people_in_frame_count = 0
    #   play video till the end
    while(cap.isOpened()):
        #   setup
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=min(600, frame.shape[1]))
        orig = frame.copy()
        (rects, weights)=hog.detectMultiScale(frame,winStride=(4,4),padding=(4, 4),scale=1.50)
        #   frame information
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        #   line in the middle of the screen
        cv2.line(frame, (300, 0), (300, 600), (0, 0, 255), 2)
        #   use centroid method of uniquely identifying objects found
        ct = CentroidTracker()
        tracked_x = deque([], maxlen=MAX_BUFFER)
        #    found objects
        for i, (x, y, w, h) in enumerate(rects):
            center = (int((x+w) - (w/2)), int((y+h) - (h/2)))
            detections.append(center)
            people_in_frame_count += 1
            cv2.circle(frame, (center), 5, (0, 0, 255), 2)
            if len(detections) > 1:
                for i in range(1, len(detections)):
                    thickness = int(np.sqrt(MAX_BUFFER/float(i+1)) * 1.80)
                    line_color = (255, 255, 0)
                    cv2.line(frame, detections[i-1], detections[i], line_color, thickness)
        # apply nms to make objects found more precise
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
        for (xA, yA, xB, yB) in pick:
            objects = ct.update(pick)
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 1)
            for i, (objectID, centroid) in enumerate(objects.items()):
                #    unique objects found persons here
                to = trackableObjects.get(objectID, None)
                if to is None:
                    to = TrackableObject(objectID, centroid)
                else:
                    if to.objectID == 0:
                        to.counted = False
                    x = [c[0] for c in to.centroids]
                    direction = centroid[0]-25 - np.mean(x)
                    #   debug lel
                    print("Centroid " + str(to.objectID) + " Xaxis " + str(centroid[0]) + " in " + str(direction) + " at " + str(round((cap.get(cv2.CAP_PROP_POS_MSEC)/1000), 2)) + " ? " + str(to.counted))
                    to.centroids.append(centroid)
                    if not to.counted:
                        if direction < 0 and centroid[0] > 297 and centroid[0] < 300:
                            left_counter += 1
                            to.counted = True
                        elif direction > 0 and centroid[0] > 301 and centroid[0] < 303:
                            right_counter += 1
                            to.counted = True
                # store the trackable object in our dictionary
                trackableObjects[objectID] = to
            #   person found label
            text = "Person {}".format(objectID)
            cv2.putText(frame,text,(centroid[0]-10,centroid[1]-10),font,0.5,(0, 0, 255),1)
        #   text
        default_frame_text(cap, frame, left_counter, right_counter, fps, people_in_frame_count)
        #   Display the resulting frame
        cv2.imshow("Bakker van Maanen", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #   When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def default_frame_text(cap, frame, left_counter, right_counter, fps, people_in_frame_count):
    duration = round((cap.get(cv2.CAP_PROP_POS_MSEC)/1000), 2)
    cv2.putText(frame, "Right counter: " + str(right_counter) , (20, 40), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, "Left counter: " + str(left_counter), (20, 60), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, "Time / FPS: " + (str(duration) + " - " + str(fps)), (20, 20), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, "Total being detected: " + str(people_in_frame_count), (400, 20), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)


#   MAGGGGICCCC
detect_people()

