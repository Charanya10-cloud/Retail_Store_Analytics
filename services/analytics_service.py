class AnalyticsService:

    def __init__(
        self,
        db
    ):

        self.db = db

    def print_summary(
        self
    ):

        cursor = self.db.cursor

        print(
            "\n===== ANALYTICS ====="
        )

        cursor.execute(
            """
            SELECT category,
                   COUNT(*)
            FROM footfall_logs
            GROUP BY category
            """
        )

        for row in cursor.fetchall():

            print(
                row
            )

        cursor.execute(
            """
            SELECT gender,
                   COUNT(*)
            FROM footfall_logs
            GROUP BY gender
            """
        )

        print(
            "\nGender Distribution"
        )

        for row in cursor.fetchall():

            print(
                row
            )

        cursor.execute(
            """
            SELECT age_group,
                   COUNT(*)
            FROM footfall_logs
            GROUP BY age_group
            """
        )

        print(
            "\nAge Group Distribution"
        )

        for row in cursor.fetchall():

            print(
                row
            )