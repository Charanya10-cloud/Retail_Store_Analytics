from utils.color_utils import calculate_blue_ratio


class EmployeeClassifier:

    def classify(self, person_crop):

        h = person_crop.shape[0]

        upper_body = person_crop[
            int(h * 0.15):int(h * 0.60),
            :
        ]

        blue_ratio = calculate_blue_ratio(
            upper_body
        )

        print(
            f"Blue Ratio: {blue_ratio:.2f}"
        )

        if blue_ratio > 0.12:
            return "Employee"

        return "Customer"