import cv2


def draw_bbox(

    frame,

    bbox,

    color,

    label

):

    x1, y1, x2, y2 = bbox

    cv2.rectangle(

        frame,

        (x1, y1),

        (x2, y2),

        color,

        2
    )

    cv2.putText(

        frame,

        label,

        (x1, y1 - 10),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.6,

        color,

        2
    )