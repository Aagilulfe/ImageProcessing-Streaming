import time
import cv2
from sh import gphoto2 as gp
import subprocess, os, signal

# CLIENT_IP = "192.168.1.102"
# dispW= 640
# dispH= 480
# flip=0

# load the cascade
face_cascade = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
trigger_command = ["--capture-image-and-download"]

# camSet='nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

# "gst-launch-1.0 nvarguscamerasrc ! 'video/x-raw(memory:NVMM), width=1920, height=1080, framerate=30/1' ! omxh264enc control-rate=2 bitrate=4000000 ! video/x-h264, stream-format=byte-stream ! rtph264pay mtu=1400 ! udpsink host=$CLIENT_IP port=5000 sync=false async=false"
# "gst-launch-1.0 udpsrc port=5000 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! h264parse ! queue ! avdec_h264 ! xvimagesink sync=false async=false -e"

cam = cv2.VideoCapture(0)
# cam = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw, framerate=20/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

# out = cv2.VideoWriter("appsrc ! video/x-raw, format=BGR ! queue ! videoconvert ! video/x-raw, format=BGRx ! nvvidconv ! omxh264enc ! video/x-h264, stream-format=byte-stream ! h264parse ! rtph264pay mtu=1400 ! udpsink host=" + CLIENT_IP + " port=5000 sync=false async=false", cv2.CAP_GSTREAMER, 0, 25.0, (1920, 1080))
# out = cv2.VideoWriter('appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=192.168.1.102 port=5000',cv2.CAP_GSTREAMER,0, 20, (dispW, dispH), True)

timestamp = time.time() - 5

while True :
    ret,frame = cam.read()
    if ret:
        # Convert into grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        print(faces)
        if (time.time() - timestamp) >= 5 and len(faces) != 0:
            print("photo taken")
            p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
            out, err = p.communicate()
            #Search for the line that has the process
            for line in out.splitlines():
                if b'gvfsd-gphoto2' in line:
                    #kill the process
                    pid = int(line.split(None,1)[0])
                    os.kill(pid, signal.SIGKILL)
            gp(trigger_command)
            timestamp = time.time()

        # Display the output
        cv2.imshow('img', frame)
        # out.write(frame)
    key = cv2.waitKey(1)
    if key==ord('q'):
        print("Quit")
        break

cam.release()
# out.release()
cv2.destroyAllWindows()