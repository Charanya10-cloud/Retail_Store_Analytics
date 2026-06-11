# tests/test_face_attributes.py

import cv2
from insightface.app import FaceAnalysis

# Load image
img = cv2.imread("tests/test.png")

if img is None:
    print("Image not found!")
    exit()

print("Image loaded successfully")
print("Shape:", img.shape)

# Load InsightFace
app = FaceAnalysis()

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)

# Detect faces
faces = app.get(img)

print(f"Faces detected: {len(faces)}")

for i, face in enumerate(faces):

    print(f"\nFace {i+1}")

    print(
        "Age:",
        face.age
    )

    print(
        "Gender:",
        face.gender
    )

    # Usually:
    # 0 = Female
    # 1 = Male

    if face.gender == 0:
        print("Gender Label: Female")
    else:
        print("Gender Label: Male")