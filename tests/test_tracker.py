import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
import cv2

from models.tracker import (
    PersonTracker
)

tracker = PersonTracker()

cap = cv2.VideoCapture(
    "data/videos/input.mp4"
)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    people = tracker.track(
        frame
    )

    for person in people:

        pid = person["id"]

        x1, y1, x2, y2 = (
            person["bbox"]
        )

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            str(pid),
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "Tracking",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()