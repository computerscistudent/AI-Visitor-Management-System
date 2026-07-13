import cv2

from app.services.recognition_service import recognize_faces,load_embeddings

known_embeddings = load_embeddings()
if len(known_embeddings) == 0:
    print("No registered visitors found.")
    exit()
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Cannot open webcam")
    exit()

while True:
    success, frames = camera.read()
    if not success:
        break
    
    faces = recognize_faces(frames, known_embeddings=known_embeddings, threshold=0.60)

    for face in faces:
        x1,y1,x2,y2 = face['bbox']
        cv2.rectangle(frames,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.putText(frames,
            f"{face['name']} ({face['confidence']:.2f})",
            (x1, y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )
    cv2.imshow("Recognition", frames)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()




















# import cv2
# import os
# from deepface import DeepFace

# camera = cv2.VideoCapture(0)

# print("Press SPACE to recognize yourself")
# print("Press Q to quit")

# while True:
#     success, frame = camera.read()

#     if not success:
#         break

#     cv2.imshow("Face Recognition", frame)

#     key = cv2.waitKey(1)

#     if key == ord(" "):
#         temp_image = "uploads/temp.jpg"
#         cv2.imwrite(temp_image,frame)

#         try : 
#             result = DeepFace.find(img_path=temp_image,db_path="dataset",model_name='OpenFace',detector_backend='opencv',enforce_detection=True)
#             print(result)
#         except Exception as e:
#             print(e)
#     elif key == ord("q"):
#         break

# camera.release()
# cv2.destroyAllWindows()
            