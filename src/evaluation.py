import os
import pandas as pd

# Configuration: Paths for solution file and student submissions
SOLUTIONS_FILE = "solutions/solution.csv"  # File with the correct answers
ASSIGNMENTS_FOLDER = "assignments/"  # Folder with student submissions
REPORT_FILE = "report.csv"  # Report with student scores

def read_csv_data(file_path):
    """Opens a CSV file in Pandas."""
    return pd.read_csv(file_path, header=None, dtype=str).fillna("")

def evaluate_submission(student_file, data_solutions):
    """Compares a student's file with the solution file and assigns a score."""
    # Split the filename by the hyphen to extract first name and last name
    student_name, student_surname = os.path.splitext(student_file)[0].split('-')
    
    # Open the student file and solution file
    student_path = os.path.join(ASSIGNMENTS_FOLDER, student_file)
    data_student = read_csv_data(student_path)

    score = 0
    total_cells = data_solutions.size

    # Compare each cell's value with the solution
    for i in range(min(len(data_solutions), len(data_student))):
        for j in range(min(len(data_solutions.columns), len(data_student.columns))):
            if data_solutions.iat[i, j] == data_student.iat[i, j]:  # Text comparison
                score += 1

    percentage = (score / total_cells) * 100
    return student_name, student_surname, round(percentage, 2)

def main():
    """Iterates through student files, evaluates them, and generates a report."""
    if not os.path.exists(ASSIGNMENTS_FOLDER):
        print(f"Error: folder '{ASSIGNMENTS_FOLDER}' not available.")
        return

    if not os.path.exists(SOLUTIONS_FILE):
        print(f"Error: file '{SOLUTIONS_FILE}' not available.")
        return
        
    data_solutions = read_csv_data(SOLUTIONS_FILE)
    results = []
  
    for file in os.listdir(ASSIGNMENTS_FOLDER):
        if file.endswith(".csv"):
            student_name, student_surname, score = evaluate_submission(file, data_solutions)
            results.append({"Name": student_name, "Surname": student_surname, "Score (%)": score})
            print(f"Evaluating {file}: {score}%")

    # Write results to CSV
    data_report = pd.DataFrame(results)
    data_report.to_csv(REPORT_FILE, index=False)
    
    print(f"Report: {REPORT_FILE}")

if __name__ == "__main__":
    main()
