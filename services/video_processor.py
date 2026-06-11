import cv2

from models.tracker import PersonTracker
from models.employee_classifier import EmployeeClassifier
from models.face_detector import FaceDetector
from models.age_gender import AgeGenderAnalyzer

from database.db import DatabaseManager

from services.analytics_service import AnalyticsService
from services.report_service import ReportService


class VideoProcessor:

    def __init__(self):

        self.tracker = PersonTracker()

        self.classifier = EmployeeClassifier()

        self.face_detector = FaceDetector()

        self.age_gender = AgeGenderAnalyzer()

        self.db = DatabaseManager()

        self.employee_count = 0

        self.customer_count = 0

        self.counted_ids = set()

        self.person_info = {}

    def process_video(
        self,
        input_path,
        output_path
    ):

        cap = cv2.VideoCapture(
            input_path
        )

        if not cap.isOpened():

            print(
                "Unable to open video."
            )

            return

        width = int(
            cap.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        height = int(
            cap.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        fps = cap.get(
            cv2.CAP_PROP_FPS
        )

        if fps == 0:
            fps = 30

        writer = cv2.VideoWriter(

            output_path,

            cv2.VideoWriter_fourcc(
                *"mp4v"
            ),

            fps,

            (
                width,
                height
            )
        )

        print(
            f"Video: {width}x{height}"
        )

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            people = self.tracker.track(
                frame
            )

            for person in people:

                pid = person["id"]

                x1, y1, x2, y2 = (
                    person["bbox"]
                )

                x1 = max(
                    0,
                    x1
                )

                y1 = max(
                    0,
                    y1
                )

                x2 = min(
                    frame.shape[1],
                    x2
                )

                y2 = min(
                    frame.shape[0],
                    y2
                )

                crop = frame[
                    y1:y2,
                    x1:x2
                ]

                if crop.size == 0:
                    continue

                category = (
                    self.classifier.classify(
                        crop
                    )
                )

                if pid not in self.person_info:

                    face = (
                        self.face_detector.detect_face(
                            crop
                        )
                    )

                    demographics = (
                        self.age_gender.analyze(
                            face
                        )
                    )

                    self.person_info[
                        pid
                    ] = demographics

                info = (
                    self.person_info[
                        pid
                    ]
                )

                gender = info[
                    "gender"
                ]

                age = info[
                    "age"
                ]

                age_group = info[
                    "age_group"
                ]

                if pid not in self.counted_ids:

                    self.counted_ids.add(
                        pid
                    )

                    if category == "Employee":

                        self.employee_count += 1

                    else:

                        self.customer_count += 1

                    self.db.log_person(

                        pid,

                        category,

                        gender,

                        age_group
                    )

                    print(
                        f"Logged Person {pid}"
                    )

                if category == "Employee":

                    color = (
                        255,
                        0,
                        0
                    )

                else:

                    color = (
                        0,
                        255,
                        0
                    )

                cv2.rectangle(

                    frame,

                    (
                        x1,
                        y1
                    ),

                    (
                        x2,
                        y2
                    ),

                    color,

                    3
                )

                cv2.putText(

                    frame,

                    f"{category} | ID {pid}",

                    (
                        x1,
                        y1 - 10
                    ),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.7,

                    color,

                    2
                )

                cv2.putText(

                    frame,

                    f"{gender} | {age} | {age_group}",

                    (
                        x1,
                        y2 + 20
                    ),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.6,

                    color,

                    2
                )

            cv2.putText(

                frame,

                f"Employees: {self.employee_count}",

                (
                    20,
                    40
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                1,

                (
                    255,
                    0,
                    0
                ),

                2
            )

            cv2.putText(

                frame,

                f"Customers: {self.customer_count}",

                (
                    20,
                    80
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                1,

                (
                    0,
                    255,
                    0
                ),

                2
            )

            cv2.putText(

                frame,

                f"Total: {self.employee_count + self.customer_count}",

                (
                    20,
                    120
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                1,

                (
                    255,
                    255,
                    255
                ),

                2
            )

            writer.write(
                frame
            )

            cv2.imshow(
                "Retail Analytics",
                frame
            )

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()

        writer.release()

        cv2.destroyAllWindows()

        analytics = AnalyticsService(
            self.db
        )

        analytics.print_summary()

        report = ReportService(
            self.db
        )

        report.generate_report()

        self.db.close()

        print(
            "\nProcessing Complete"
        )