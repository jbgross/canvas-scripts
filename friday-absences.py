import pandas as pd
import sys

if len(sys.argv) != 2:
    print("Usage: python friday_absences.py <attendance_report.csv>")
    sys.exit(1)

file_path = sys.argv[1]

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    sys.exit(1)
except pd.errors.EmptyDataError:
    print(f"Error: The file '{file_path}' is empty.")
    sys.exit(1)
except Exception as e:
    print(f"Error: An unexpected error occurred while reading the file: {e}")
    sys.exit(1)

# Adjust these column names if your Canvas report uses different labels
date_column = "Class Date"
status_column = "Attendance"

df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
df = df.dropna(subset=[date_column])

# Keep only Fridays
friday_rows = df[df[date_column].dt.day_name() == "Friday"]

# Keep only absences
friday_absences = friday_rows[
    friday_rows[status_column].astype(str).str.lower() == "absent"
]

total_friday_absences = len(friday_absences)

print(f"Total number of absences on Fridays: {total_friday_absences}")