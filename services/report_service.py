import os
import pandas as pd
from datetime import datetime


class ReportService:

    def __init__(
        self,
        db
    ):

        self.db = db

    def generate_report(self):

        os.makedirs(
            "data/reports",
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        # CSV REPORT

        query = """
        SELECT
            person_id,
            category,
            gender,
            age_group,
            timestamp
        FROM footfall_logs
        """

        df = pd.read_sql_query(
            query,
            self.db.conn
        )

        csv_file = (
            f"data/reports/footfall_report_{timestamp}.csv"
        )

        df.to_csv(
            csv_file,
            index=False
        )

        print(
            f"CSV Saved: {csv_file}"
        )

        # TXT SUMMARY REPORT

        txt_file = (
            f"data/reports/summary_{timestamp}.txt"
        )

        with open(
            txt_file,
            "w",
            encoding="utf-8"
        ) as report:

            report.write(
                "FOOTFALL ANALYTICS REPORT\n"
            )

            report.write(
                "=" * 50
            )

            report.write(
                "\n\n"
            )

            report.write(
                f"Total Records : {len(df)}\n\n"
            )

            report.write(
                "CATEGORY COUNTS\n"
            )

            report.write(
                "-" * 30 + "\n"
            )

            category_counts = (
                df["category"]
                .value_counts()
            )

            for category, count in category_counts.items():

                report.write(
                    f"{category}: {count}\n"
                )

            report.write("\n")

            report.write(
                "GENDER COUNTS\n"
            )

            report.write(
                "-" * 30 + "\n"
            )

            gender_counts = (
                df["gender"]
                .value_counts()
            )

            for gender, count in gender_counts.items():

                report.write(
                    f"{gender}: {count}\n"
                )

            report.write("\n")

            report.write(
                "AGE GROUP COUNTS\n"
            )

            report.write(
                "-" * 30 + "\n"
            )

            age_counts = (
                df["age_group"]
                .value_counts()
            )

            for age, count in age_counts.items():

                report.write(
                    f"{age}: {count}\n"
                )

        print(
            f"TXT Saved: {txt_file}"
        )