import numpy as np
import supervision as sv

from models.detector import PersonDetector


class PersonTracker:

    def __init__(self):

        self.detector = PersonDetector()

        self.tracker = sv.ByteTrack(
            track_activation_threshold=0.25
        )

    def track(self, frame):

        detections = self.detector.detect(
            frame
        )

        if len(detections) == 0:
            return []

        xyxy = np.array(
            [d["bbox"] for d in detections],
            dtype=np.float32
        )

        confidence = np.array(
            [d["confidence"] for d in detections],
            dtype=np.float32
        )

        class_id = np.zeros(
            len(detections),
            dtype=int
        )

        detections_sv = sv.Detections(
            xyxy=xyxy,
            confidence=confidence,
            class_id=class_id
        )

        tracked = (
            self.tracker.update_with_detections(
                detections_sv
            )
        )

        people = []

        if tracked.tracker_id is None:
            return []

        for bbox, track_id in zip(
            tracked.xyxy,
            tracked.tracker_id
        ):

            x1, y1, x2, y2 = map(
                int,
                bbox
            )

            people.append(
                {
                    "id": int(track_id),
                    "bbox": (
                        x1,
                        y1,
                        x2,
                        y2
                    )
                }
            )

        return people