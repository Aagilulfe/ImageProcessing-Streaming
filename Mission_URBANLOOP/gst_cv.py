import cv2
import matplotlib.pyplot as plt

# RaspiStreamCam=cv2.VideoCapture('tcpclientsrc host=192.168.1.37 port=5000 ! gdpdepay ! rtph264depay ! h264parse ! omxh264dec ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink', 1800)
RaspiStreamCam=cv2.VideoCapture('gst-launch-1.0 -v tcpclientsrc host=192.168.1.64 port=5000  ! jpegdec ! xvimagesink', 1800)

while True:

    ret, frameRaspiIP=RaspiStreamCam.read()
    try:
        cv2.imshow('RaspiStreamCam',frameRaspiIP)
    except:
        print("empty frame")
        continue

    if cv2.waitKey(1)==ord('q'):
        break

RaspiStreamCam.release()

cv2.destroyAllWindows()