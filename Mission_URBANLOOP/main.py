import cv2
import numpy as np
 
# initialisation du HOG:
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture("tcp://192.168.1.95:5000")

font = cv2.FONT_HERSHEY_SIMPLEX

i = 0

while True:
    ret, frame = cap.read()
    if ret:

        # réduction de l'image pour une détection plus rapide
        # frame = cv2.resize(frame, (640, 480))
        # passage en noir et blanc, également pour accélerer 
        # la détection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
        # détection des personnes dans l'image. 
        # retourne les coordonnées de la boîte encadrant 
        # les personnes détectées
        boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        for (xA, yA, xB, yB) in boxes:
            # affichages des boîtes sur l'image couleur
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
    
        # écriture de la vidéo avec les boîtes
        # out.write(frame.astype('uint8'))

        # affichage de l'image résultante
        cv2.imshow('Video Capture', frame)
        i += 1
        print("Frame analyzed: ", i)

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

print("[INFO] cleaning up...")
cap.release()
cv2.destroyAllWindows()