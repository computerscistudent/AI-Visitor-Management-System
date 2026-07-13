from app.services.capture_service import capture_images
from app.services.embedding_service import generate_embeddings

name = input("Enter visitor name: ").strip()

if not name:
    print("Invalid name.")
    exit()

captured = capture_images(name)

if not captured:
    print("Image capture failed.")
    exit()

generated = generate_embeddings(name)

if not generated:
    print("Embedding generation failed.")
    exit()

print("\n✅ Visitor registered successfully!")
