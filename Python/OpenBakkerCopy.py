import numpy as np
import cv2
from collections import deque
import time
import datetime
import imutils
from imutils.video import VideoStream
from imutils.object_detection import non_max_suppression
from imutils.video import FPS
from picamera import PiCamera
import datetime
import Bakkerbase

#   junk
font = cv2.FONT_HERSHEY_SIMPLEX
MAX_BUFFER = 64


def take_picture():
    camera = PiCamera()
    camera.resolution = (600, 600)
    time.sleep(5)
    camera.capture('people.jpg')


def detect_smiles():
    take_picture()
    img = cv2.imread('smiles.jpg')
    img = cv2.flip(img, -1)
    frame = imutils.resize(img, width=min(600, img.shape[1]))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    smiles = smile_cascade.detectMultiScale(frame, scaleFactor=1.90, minNeighbors=4, minSize=(30, 30), maxSize=(70, 70))
    for(x, y, w, h) in smiles:
        cv2.rectangle(frame, (x, y), ((x+w), (y+h)), (0, 255, 0), 2)
    if smiles is None:
        return 0
    else:
        print(len(smiles))
        cv2.imwrite('smiles-detected.jpg', frame)
    #   Frame
    cv2.imshow("Bakker van Maanen", frame)
    cv2.waitKey(0)


def detect_people():
    #   start time, for logging purposes. can be pushed.
    print(datetime.datetime.now())
    #   initialize HOG people detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    #   variables to be used to send to firebase.
    detections_x = []
    detections_y = []
    coords_x = []
    coords_y = []
    #   amount of people detected divided by the time passed
    average_waiting_time = 0
    #   try and keep track of previous amount of people to avoid doubles
    last_people_counter = 0
    #   counters
    people_counter = 0
    amount_found = 0
    #   every TIME_INTERVAL increment to use for choose -> current_time_counter = 3 -> 30 aprox seconds.
    current_time_counter = 0
    #   sample rate of coords
    COORDS_SAMPLE_RATE = 10
    #   amount of samples per 10 seconds, tested.
    TIME_SAMPLE_RATE = 7 * 1.25
    #   what should we do after every 10 seconds?
    TIME_INTERVAL = 10
    #   to be used to divide the amount of people found and seconds it took for samples to be collected
    TIME_WAITING = 60
    #   idle time
    idle_time = 0
    person_found_time_counter = 0
    # camera setup
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(1)
    start_time = time.time()
    #   play video till the end
    while True:
        #   each time we loop determine time spent. this is used to keep track of time.
        end_time = time.time()
        current_time_elapsed = end_time - start_time
        #   if 10 seconds has passed
        if int(current_time_elapsed) > TIME_INTERVAL:
            #   DO CHECKS BEFORE RESETTING VALUES
            #   10 seconds = 1
            current_time_counter += 1
            #   modulo of 6 is that it can push data after every 60 seconds.
            #   we want to push every 5 minutes
            if current_time_counter % 6 is 0:
                #   time spent = total clients / 5minutes?
                #   no clients? can't divide by 0 now can we
                try:
                   if person_found_time_counter < 2 and person_found_time_counter is not 0:
                       idle_time = ((person_found_time_count * 10) / amount_found)
                   idle_time = (TIME_WAITING / amount_found)
                except ZeroDivisionError:
                    print("No customers in the last minute")
                    idle_time = 0
                    pass
                #   push centroids
                #   push to firebase
                #   reset values of current_time_elapsed and amount_found
                if amount_found is not 0:
                    try:
                        Bakkerbase.save_klanten(idle_time, amount_found, coords_x, coords_y)
                    except ConnectionError:
                        continue
            #   if the counter divided by the samples taken in X amount of time is rounded to > 1 then
            #   add the number to the current amount_found variable
            if round(people_counter / TIME_SAMPLE_RATE) > 0:
                #   add amount of people found
                amount_found += round(people_counter / TIME_SAMPLE_RATE)
                person_found_time_counter = current_time_counter
                print("Last counted: " + str(last_people_counter))
                print("Current people counter: " + str(people_counter))
                print("Current counted: " + str(round(people_counter / TIME_SAMPLE_RATE)))
            #   trying to keep track of the last recorded people_counter to avoid doubles
            #   if the counter of the amount of people counter is equal to the last amount
            #   they are most likely idling there. otherwise the values would be slightly different
            if int(people_counter) is int(last_people_counter):
                amount_found -= amount_found
                print("People counted: " + str(amount_found))
            #   RESET THE PEOPLE COUNTER, AND START TIME
            #   THIS IS OUR INTERVAL
            print("10 Seconds Passed")
            last_people_counter = people_counter
            people_counter = 0
            start_time = time.time()
        #   CAMERA SETTINGS
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        frame = cv2.flip(frame, -1)
        #   HOG DETECTION
        (rects, weights)=hog.detectMultiScale(frame,winStride=(4,4),padding=(8, 8),scale=1.15)
        #    found objects
        for x, y, w, h in rects:
            #   get the center of the found object x and y coords, to be pushed to firebase
            center_x = int((x+w) - (w/2))
            center_y = int((y+h) - (h/2))
            #   if x is not 0 ->
            if x is not 0:
                detections_x.append(center_x)
                #   when we have enough samples
                if len(detections_x) is COORDS_SAMPLE_RATE:
                    coords_x.append(sum(detections_x)/len(detections_x))
                    del detections_x[:]
            if y is not 0:
                detections_y.append(center_y)
                #   when we have enough samples
                if len(detections_y) is COORDS_SAMPLE_RATE:
                    coords_y.append(sum(detections_y)/len(detections_y))
                    del detections_y[:]
        # apply nms to make objects found more precise
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.50)
        #   if len(pick) > 0 means we have detected a person.
        if len(pick) > 0:
            people_counter += len(pick)
        #   draw square on object. optional.
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 1)
        #   Display the resulting frame
        cv2.imshow("Bakker van Maanen", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    #   When everything done, release the capture
    cv2.destroyAllWindows()

#   MAGGGGICCCC
detect_people()
