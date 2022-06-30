import cv2

# CLIENT_IP = "192.168.1.63" #IP of Acer at home
CLIENT_IP = "192.168.1.64" #IP of Hp at home
# CLIENT_IP = "192.168.1.95" #IP of Jetson at home
CLIENT_PORT = 5000
dispW= 640
dispH= 480
flip=2

# load the cascade for face detection
face_cascade = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

camSet='nvarguscamerasrc ! video/x-raw(memory:NVMM), width=640, height=480, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(camSet)
out = cv2.VideoWriter('appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host='+CLIENT_IP+' port='+str(CLIENT_PORT),cv2.CAP_GSTREAMER,0, 20, (dispW, dispH), True)

while True :
    ret,frame = cam.read()
    if ret: # frame captured without any errors
        # Convert into grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Display the output
        cv2.imshow('img', frame) # comment to disable local display
        # Send to the client
        out.write(frame)
    key = cv2.waitKey(1)
    if key==ord('q'):   # exit on 'q' pressed
        print("Quit")
        break

cam.release()   # release the camera
out.release()   # release the stream
cv2.destroyAllWindows()