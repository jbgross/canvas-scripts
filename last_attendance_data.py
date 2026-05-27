import pandas as pd
import sys

# Check if the correct number of command-line arguments are provided
if len(sys.argv) != 2:
    print("Usage: python script_name.py <attendance_report.csv>")
    sys.exit(1)

# Get the input file path from the command-line argument
file_path = sys.argv[1]

# Try to read the CSV file into a pandas DataFrame
try:
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

# Keep only rows where Attendance is "present"
df = df[df['Attendance'].str.lower() == 'present']
print(df)

# Convert Class Date to datetime
df['Class Date'] = pd.to_datetime(df['Class Date'], errors='coerce')

# Filter out rows where the date couldn't be parsed
df = df.dropna(subset=['Class Date'])

# Group by student name and get the last attendance date
last_attendance = df.groupby('Student Name')['Class Date'].max().reset_index()

# Sort the results if needed (optional)
last_attendance = last_attendance.sort_values(by='Class Date', ascending=False)

# Format the date as MM/DD/YYYY
last_attendance['Class Date'] = last_attendance['Class Date'].dt.strftime('%m/%d/%Y')

# Display the results
# print(last_attendance)

# Optionally, save the results to a new CSV file
output_filename = "last_attendance_report.csv"
last_attendance.to_csv(output_filename, index=False)

print(f"Results saved to {output_filename}")