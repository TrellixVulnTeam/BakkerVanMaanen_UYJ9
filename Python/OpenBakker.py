import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np


# CAMERA CONSTANTS
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
# cascades for detection recognition
fullBodyCascade = cv2.CascadeClassifier('cascades/haarcascade_fullbody.xml')
eyeCascade = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')
facesCascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
# PiCamera setup
camera = PiCamera()
camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
camera.framerate = 32
# camera.zoom = (0.25, 0.25, 0.60, 0.60)
rawCapture = PiRGBArray(camera, size=(CAMERA_WIDTH, CAMERA_HEIGHT))
# Warm up camera
time.sleep(0.5)


def detect_objects():
    # left and right object detection counter
    left = 0
    right = 0
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # PiCamera image array for cv2 use
        image = frame.array
        # line for future use
        cv2.line(image, (363, 408), (465, 300), (255, 0, 0), 1)
        # Gray PiCamera output for detection use.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # full bodies cascade
        fullBodies = fullBodyCascade.detectMultiScale(
            gray,
            scaleFactor=1.10,
            minNeighbors=3,
            minSize=(5,5)
            )
        # face cascade
        faces = facesCascade.detectMultiScale(
            gray,
            scaleFactor=1.50,
            minNeighbors=5,
            minSize=(30, 30)
            )
        # For all matches in fullbodies
        for (x, y, width, height) in fullBodies:
            cv2.rectangle(image,(x, y),(x + width,  y + height), (0 , 255, 0), 1)
            # ROI = Region of Interest, aldus waar de object zich nu bevind
            roi_gray = gray[y:y+height, x:x+width]
            roi_color = image[y:y+height, x:x+width]
        # For all faces in de video
        for (x, y, width, height) in faces:
            # x = left top corner X of where object is found
            center_x = int((x+width) - (width/2))
            # y = left top corner Y of where object is found
            center_y = int((y+height) - (height/2))
            # check if object found is on the left or right side of the image (camera pov)
            if(center_x < (640/2)):
                left += 1
            else:
                right += 1
            # cv2.rectangle(image,(x, y),(x + width, y + height), (0,0,255), 1)
            cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)
            roi_gray = gray[y:y+height, x:x+width]
            roi_color = image[y:y+height, x:x+width]
            # print object direction counter
            print("Left count: " + str(left) + " Right counter: " + str(right))
        # Show stream in console
        cv2.imshow("Bakker van Maanen", image)
        # Press q to exit the video stream
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            break


if __name__ == "__main__":
    detect_objects()

