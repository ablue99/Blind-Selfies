import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


cv2.namedWindow('capture')
# first need to get the frame from the webcamera and then change to grey

cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()  # would have a bool for if it was read correctly, we don't care :) Or maybe we do, who knows

grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
face_coords = face_cascade.detectMultiScale(grey_frame, 1.2,
                                            5)  # detect the face, return coordinates, may have more than one face
# need to go through those faces and draw squares around each one
for (x, y, w, h) in face_coords:
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow('capture', frame)

# cv2.waitkey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()