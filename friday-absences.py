import pandas as pd
import sys

if len(sys.argv) != 2:
    print("Usage: python friday_absences.py <attendance_report.csv>")
    sys.exit(1)

file_path = sys.argv[1]

try:
    # df = pd.read_csv(file_path)
    df = pd.read_csv(file_path, usecols=range(14))
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
print(df[[date_column]].head())
print()
df[date_column] = pd.to_datetime(
    df[date_column].astype(str).str.strip(),
    format="%Y-%m-%d",
    errors="coerce"
)

# print(df[[date_column]].head())
# print(df[date_column].dt.weekday.head())
df = df.dropna(subset=[date_column])

total = len(df)
print(f"Total number of absences on Fridays: {total}")

# Keep only Fridays
friday_rows = df[df[date_column].dt.weekday == 4]

total_friday = len(friday_rows)
print(f"Total number of absences on Fridays: {total_friday}")
# Keep only absences
friday_absences = friday_rows[
    friday_rows[status_column].astype(str).str.lower() == "absent"
]

total_friday_absences = len(friday_absences)

print(f"Total number of absences on Fridays: {total_friday_absences}")
student_column = "Student Name"

absence_counts = (
    friday_absences
    .groupby(student_column)
    .size()
    .to_dict()
)

for key, value in absence_counts.items():
    if value > 2:
        print(f"{key}: {value}")