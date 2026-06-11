from datetime import datetime


class ReportService:

    def __init__(
        self,
        db
    ):

        self.db = db

    def generate_report(
        self
    ):

        cursor = self.db.cursor

        report_name = (

            "data/output/report_"

            +

            datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            +

            ".txt"
        )

        with open(

            report_name,

            "w",

            encoding="utf-8"

        ) as report:

            report.write(
                "FOOTFALL ANALYTICS REPORT\n"
            )

            report.write(
                "=" * 40
            )

            report.write(
                "\n\n"
            )

            cursor.execute(
                """
                SELECT category,
                       COUNT(*)
                FROM footfall_logs
                GROUP BY category
                """
            )

            report.write(
                "CATEGORY COUNTS\n"
            )

            for row in cursor.fetchall():

                report.write(
                    f"{row[0]} : {row[1]}\n"
                )

            report.write(
                "\n"
            )

            cursor.execute(
                """
                SELECT gender,
                       COUNT(*)
                FROM footfall_logs
                GROUP BY gender
                """
            )

            report.write(
                "GENDER COUNTS\n"
            )

            for row in cursor.fetchall():

                report.write(
                    f"{row[0]} : {row[1]}\n"
                )

            report.write(
                "\n"
            )

            cursor.execute(
                """
                SELECT age_group,
                       COUNT(*)
                FROM footfall_logs
                GROUP BY age_group
                """
            )

            report.write(
                "AGE GROUP COUNTS\n"
            )

            for row in cursor.fetchall():

                report.write(
                    f"{row[0]} : {row[1]}\n"
                )

        print(
            f"\nReport Saved: {report_name}"
        )