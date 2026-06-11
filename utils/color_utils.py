import cv2
import numpy as np


def calculate_blue_ratio(
    image
):

    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    lower_blue = np.array(
        [90, 50, 50]
    )

    upper_blue = np.array(
        [140, 255, 255]
    )

    mask = cv2.inRange(

        hsv,

        lower_blue,

        upper_blue
    )

    blue_pixels = cv2.countNonZero(
        mask
    )

    total_pixels = (
        image.shape[0]
        *
        image.shape[1]
    )

    return (
        blue_pixels
        /
        total_pixels
    )