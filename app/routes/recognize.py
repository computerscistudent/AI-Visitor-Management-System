from flask import Blueprint , render_template
import cv2
from app.services.recognition_service import load_embeddings,recognize_faces
import time

recognize_bp = Blueprint("recognize",__name__)

@recognize_bp.route("/recognize")
def recognize():
    print("0. Route entered")
    known_embeddings = load_embeddings()
    print("1. Embeddings loaded")
    camera = cv2.VideoCapture(0,cv2.CAP_ANY)
    print("2. Camera object created")
    if not camera.isOpened():
        print("3. Camera failed")
        return "Cannot open webcam."
    
    print("4. Camera opened")
    while True:
        print("5A Before camera.read()")
        success,frame = camera.read()
        print("5B After camera.read()")
        if not success:
            break
        
        print("6. Got frame")
        faces = recognize_faces(frame=frame, known_embeddings=known_embeddings)
        print("7. Recognition complete")

        print("7.1 Before drawing")
        for face in faces:
            x1,y1,x2,y2 = face["bbox"]
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(frame,
            f"{face['name']} ({face['confidence']:.2f})",
            (x1, y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2)
        print("7.2 Before imshow")
        cv2.imwrite("temp.jpg", frame)

        print("saved")

        time.sleep(5)
        break
    print("9. Releasing camera")
    camera.release()
    del camera
    cv2.destroyWindow("Face Recognition")
    cv2.waitKey(100)
    print("10. Rendering HTML")

    return render_template("recognize.html")
    
