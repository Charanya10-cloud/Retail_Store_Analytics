import cv2
from insightface.app import FaceAnalysis


class FaceDetector:

    def __init__(self):

        self.app = FaceAnalysis()

        self.app.prepare(
            ctx_id=0,
            det_size=(640, 640)
        )

    def detect_face(
        self,
        image
    ):

        try:

            faces = self.app.get(
                image
            )

            if len(faces) == 0:
                return None

            return faces[0]

        except Exception:

            return None