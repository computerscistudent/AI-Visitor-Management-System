from insightface.app import FaceAnalysis
import os
import cv2
import numpy as np
from app.services.embedding_service import generate_embeddings

DATASET_DIR = "app/dataset"
EMBEDDING_DIR = "app/embeddings"

for person_name in os.listdir(DATASET_DIR):
    person_path = os.path.join(DATASET_DIR, person_name)

    if os.path.isdir(person_path):
        generate_embeddings(person_name)

if os.path.exists(EMBEDDING_DIR):
    for file in os.listdir(EMBEDDING_DIR):
        if file.endswith('.npy'):
            file_path = os.path.join(EMBEDDING_DIR, file)
            stored_embedding = np.load(file_path)
            print(f"File: {file} | Shape: {stored_embedding.shape}")
else:
    print("Embeddings directory does not exist yet.")

print("\nDone!")
