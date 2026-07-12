from insightface.app import FaceAnalysis

print("Loading InsightFace model...")

app = FaceAnalysis(name="buffalo_l")

app.prepare(ctx_id=0, det_size=(640, 640))

print("Model loaded successfully!")