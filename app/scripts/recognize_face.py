from insightface.app import FaceAnalysis
import cv2
import numpy as np
import os

app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0)

EMBEDDING_DIR = "app/embeddings"

known_embeddings = {}

for file in os.listdir(EMBEDDING_DIR):
    if file.endswith('.npy'):
        person_name = file.replace('.npy','')
        embedding = np.load(os.path.join(EMBEDDING_DIR,file))
        known_embeddings[person_name] = embedding # type:ignore
    
print(known_embeddings.keys())

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Cannot open webcam")
    exit()

def cosine_similarity(a,b):
    return np.dot(a,b) ## you can also use np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)) for normalized cosine similarity if you didnt normalize the embeddings before saving them.

while True:
    success, frames = camera.read()
    if not success:
        break
    
    faces = app.get(frames)
    for face in faces:
        bbox = face.bbox.astype(int)
        x1,y1,x2,y2 = bbox

        current_embedding = face.embedding
        current_embedding = current_embedding/np.linalg.norm(current_embedding) 

        best_name = "unknown"
        best_score = -1

        for person_name, saved_embedding in known_embeddings.items():
            similarity = cosine_similarity(saved_embedding,current_embedding)
            # print(f"{person_name}: {similarity:.4f}")

            if similarity > best_score:
                best_score = similarity
                best_name = person_name
            
        if best_score < 0.60:
            best_name = "Unknown"

        cv2.rectangle(frames,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.putText(frames,
            f"{best_name} ({best_score:.2f})",
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
            