from insightface.app import FaceAnalysis
import numpy as np
import os
from app.config import EMBEDDING_DIR
from app.services.attendance_service import mark_attendence

app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0)

def load_embeddings():
    known_embeddings = {}

    if not os.path.exists(EMBEDDING_DIR):
        return known_embeddings

    for file in os.listdir(EMBEDDING_DIR):
        if file.endswith(".npy"):
            person_name = file.replace(".npy", "")
            embedding = np.load(os.path.join(EMBEDDING_DIR, file))
            known_embeddings[person_name] = embedding

    return known_embeddings

def cosine_similarity(a,b):
    return np.dot(a,b) ## you can also use np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)) for normalized cosine similarity if you didnt normalize the embeddings before saving them.

marked_today = set()
def recognize_faces(frame, known_embeddings=None, threshold=0.60):
    if known_embeddings is None:
        known_embeddings = load_embeddings()
    faces = app.get(frame)
    results = []
    for face in faces:
        current_embedding = face.embedding
        current_embedding = (
            current_embedding /
            np.linalg.norm(current_embedding)
        )
        best_name = "Unknown"
        best_score = -1

        for person_name, saved_embedding in known_embeddings.items():
            similarity = cosine_similarity(
                saved_embedding,
                current_embedding
            )
             
            if similarity > best_score:
                best_score = similarity
                best_name = person_name
        
        if best_score < threshold:
            best_name = "Unknown"
        
        if best_name!="Unknown":
            if best_name not in marked_today:
                mark_attendence(best_name)
                marked_today.add(best_name)

        results.append({
            "name": best_name,
            "confidence": float(best_score),
            "bbox": face.bbox.astype(int)
        })

    return results