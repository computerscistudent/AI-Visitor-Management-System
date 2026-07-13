from insightface.app import FaceAnalysis
import os
import cv2
import numpy as np
from app.config import EMBEDDING_DIR , DATASET_DIR

app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=1)

os.makedirs(EMBEDDING_DIR,exist_ok=True)

def generate_embeddings(person_name, overwrite=False):
    """
    Generate one normalized embedding for a person
    using all images inside app/dataset/person_name/
    """

    embedd_file = f'{person_name}.npy'
    embedd_path = os.path.join(EMBEDDING_DIR,embedd_file)
    if os.path.exists(embedd_path) and not overwrite:
        print(f'Embedding for {person_name} already exists.')
        return True
    
    if os.path.exists(embedd_path) and overwrite:
        print(f'[INFO] Overwrite triggered! Recalculating embedding for {person_name}...')
        
    folder_path = os.path.join(DATASET_DIR,person_name)
    if not os.path.exists(folder_path):
        print(f'{person_name} not found.')
        return False

    embeddings = []

    print(f"\nGenerating embedding for {person_name}...")
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path,image_name)
        image = cv2.imread(image_path)
        if image is None:
            continue
        faces = app.get(image)

        if len(faces) == 0:
            continue

        embedding = faces[0].embedding
        embeddings.append(embedding)

    if len(embeddings) == 0 :
        print("No faces found.")
        return False
    
    embeddings = np.array(embeddings)
    mean_embedding = np.mean(embeddings, axis=0)
    mean_embedding = mean_embedding/np.linalg.norm(mean_embedding)

    save_path = os.path.join(
        EMBEDDING_DIR,
        f"{person_name}.npy"
    )

    np.save(save_path,mean_embedding)

    print("Embedding saved successfully.")

    return True



