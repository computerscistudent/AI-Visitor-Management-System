import cv2 
import os

person = "Abhimanyu"
save_path = os.path.join("app/dataset",person)
os.makedirs(save_path,exist_ok=True)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

camera = cv2.VideoCapture(0)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(BASE_DIR,'..','..',"haarcascade_frontalface_default.xml")
xml_path = os.path.normpath(xml_path)
face_detector = cv2.CascadeClassifier(xml_path)

count = 0

print("Press SPACE to capture an image")
print("Press Q to quit")

while True:
    success , frames = camera.read()
    if not success:
        break

    gray = cv2.cvtColor(frames,cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(50,50))
    for (x,y,w,h) in faces:
        cv2.rectangle(frames,(x,y),(x+w , y+h),(0,255,0),2)

    cv2.imshow("Capture Faces",frames)

    key = cv2.waitKey(1)
    if key == ord(" "):
        if(len(faces)==0):
            print("No face detected")
            continue
        x,y,w,h = faces[0]
        face = frames[y:y+h , x:x+w]
        image_path = os.path.join(save_path, f'img_{count}.jpg')
        cv2.imwrite(image_path,face)
        print(f"Saved {image_path}")

        count += 1
    elif key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
