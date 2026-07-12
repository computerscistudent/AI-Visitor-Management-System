import cv2
import os

camera = cv2.VideoCapture(0)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
face_detector = cv2.CascadeClassifier(xml_path)

while True:
    success , frames = camera.read()
    if not success:
        break
    gray = cv2.cvtColor(frames,cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(50, 50))

    for (x,y,w,h) in faces:
        cv2.rectangle(frames,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2)
    
    cv2.imshow("Face Detection", frames)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()