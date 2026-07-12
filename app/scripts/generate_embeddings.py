from insightface.app import FaceAnalysis
import os
import cv2
import numpy as np

app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=1)

DATASET_DIR = "app/dataset"
EMBEDDING_DIR = "app/embeddings"

os.makedirs(EMBEDDING_DIR,exist_ok=True)

for person_name in os.listdir(DATASET_DIR):
    person_folder = os.path.join(DATASET_DIR, person_name)
    if not os.path.isdir(person_folder):
        continue
    embeddings = []
    print(f"\nProcessing {person_name}...")
    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)
        image = cv2.imread(image_path)

        if image is None:
            continue

        faces = app.get(image)
        if len(faces) == 0:
            continue

        print(type(faces[0]))
        print(faces[0].keys())

        embedding = faces[0].embedding
        embeddings.append(embedding)

        print(type(faces[0].embedding))
        print(faces[0].embedding.shape)

    if len(embeddings) == 0 :
        print("No faces found.")
        continue
    embeddings = np.array(embeddings)
    mean_embedding = np.mean(embeddings,axis=0)
    mean_embedding = mean_embedding/np.linalg.norm(mean_embedding)

    save_path = os.path.join(
        EMBEDDING_DIR,
        f"{person_name}.npy"
    )
    np.save(save_path,mean_embedding)
    print(f"Saved embedding -> {save_path}")

print("\nDone!")
