from insightface.app import FaceAnalysis

app = FaceAnalysis()

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)

print("InsightFace Loaded Successfully")