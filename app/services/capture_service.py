import cv2
import os
from app.config import DATASET_DIR

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(BASE_DIR,'..','..',"haarcascade_frontalface_default.xml")
xml_path = os.path.normpath(xml_path)

def capture_images(person_name, num_images=20):
    person_folder = os.path.join(DATASET_DIR, person_name)
    os.makedirs(person_folder, exist_ok=True)

    camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    if not camera.isOpened():
        print("Cannot open webcam.")
        return False
    
    face_detector = cv2.CascadeClassifier(xml_path)
    print("\nPress SPACE to capture an image.")
    print("Press Q to quit.\n")

    count = 0

    while True:
        success, frames = camera.read()

        if not success:
            break

        cv2.imshow("Capture Faces", frames)

        gray = cv2.cvtColor(frames,cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(50,50))

        for (x,y,w,h) in faces:
            cv2.rectangle(frames,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.imshow("Capture Faces",frames)
        key = cv2.waitKey(1)
        if key==ord(" "):
            if len(faces) == 0:
                print("No faces found!!")
                continue
            largest_face = max(faces, key=lambda f: f[2] * f[3])
            x,y,w,h = largest_face
            face = frames[y:y+h , x:x+w]

            image_path = os.path.join(person_folder, f"img_{count+1:03d}.jpg")
            cv2.imwrite(image_path,face)
            print(f"Saved {image_path}")
            count += 1
            if count>=num_images:
                break
        elif key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    print(f"\nCaptured {count} images.")

    return count > 0