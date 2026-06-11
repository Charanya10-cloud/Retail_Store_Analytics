class AgeGenderAnalyzer:

    def analyze(
        self,
        face
    ):

        if face is None:

            return {

                "gender": "Unknown",

                "age": 0,

                "age_group": "Unknown"
            }

        age = int(
            face.age
        )

        gender = (

            "Male"

            if face.gender == 1

            else "Female"
        )

        return {

            "gender": gender,

            "age": age,

            "age_group":
            self.get_age_group(
                age
            )
        }

    def get_age_group(
        self,
        age
    ):

        if age <= 12:
            return "Child"

        elif age <= 25:
            return "Youth"

        elif age <= 60:
            return "Adult"

        return "Senior"