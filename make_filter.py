#! /usr/local/bin/python3
from __future__ import print_function
import cv2 as cv
import argparse
import time

# https://docs.opencv.org/4.x/da/d97/tutorial_threshold_inRange.html

max_value = 100
max_value_H = 360
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

## [low]
def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    print (f'low H -{val}')
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
## [low]

## [high]
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    print (f'high H -{val}')
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
## [high]

def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    print (f'low S -{val}')
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)

def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    print (f'high S -{val}')
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)

def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    print (f'low V -{val}')
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)

def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    print (f'high V -{val}')
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)

parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera divide number.', default=0, type=int)
args = parser.parse_args()

## [cap]
cap =  cv.VideoCapture("Rolling.mov")
## [cap]

## [window]
cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)
## [window]

## [trackbar]
cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)
## [trackbar]


ret, frame = cap.read()
cv.imshow(window_capture_name, frame)

gimage = cv.imread('green.jpg')
while True:
    ## [while]

    # if frame is None:
    #     break
    # OpenCV halves the H values to fit the range [0,255],
    # so H value instead of being in range [0, 360], is in range [0, 180]. S and V are still in range [0, 255].
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))

    for h in range(0,180,5):
        for s in range(0,255,5):
            for v in range (0,255,5):
                print (f'{h} {s} {v}')
                frame_threshold = cv.inRange(frame_HSV, (h,s,v), (100, 100, 250))
    ## [while]

                ## [show]
                # cv.imshow(window_capture_name, frame)
                cv.imshow(window_detection_name, frame_threshold)
                ## [show]
                time.sleep(0.5)

                key = cv.waitKey(30)
                if key == ord('q') or key == 27:
                    print (low_H,high_H,low_S,high_S,low_V,high_V)
                    break