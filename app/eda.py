import os
import pandas as pd


def generate_eda_report(df, report_path):
    """
    Generate a basic Exploratory Data Analysis (EDA) report.
    """

    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:

        f.write("=" * 60 + "\n")
        f.write("LOAN ELIGIBILITY DATASET - EDA REPORT\n")
        f.write("=" * 60 + "\n\n")

        # Dataset Shape
        f.write("1. Dataset Shape\n")
        f.write("-" * 30 + "\n")
        f.write(f"Rows    : {df.shape[0]}\n")
        f.write(f"Columns : {df.shape[1]}\n\n")

        # Column Information
        f.write("2. Column Information\n")
        f.write("-" * 30 + "\n")
        f.write(df.dtypes.to_string())
        f.write("\n\n")

        # Missing Values
        f.write("3. Missing Values\n")
        f.write("-" * 30 + "\n")
        f.write(df.isnull().sum().to_string())
        f.write("\n\n")

        # Duplicate Rows
        f.write("4. Duplicate Rows\n")
        f.write("-" * 30 + "\n")
        f.write(f"{df.duplicated().sum()}\n\n")

        # Statistical Summary
        f.write("5. Numerical Summary\n")
        f.write("-" * 30 + "\n")
        f.write(df.describe().to_string())
        f.write("\n\n")

    print(f"EDA Report saved successfully at:\n{report_path}")