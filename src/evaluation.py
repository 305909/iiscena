import os
import sys
import pandas as pd

def get(folder_path):
    """Find the last available folder in the directory."""
    subdirs = [
        os.path.join(folder_path, d) for d in os.listdir(folder_path) 
        if os.path.isdir(os.path.join(folder_path, d))
    ]
    if not subdirs:
        return None
    return max(subdirs, key=os.path.getmtime)

def read(file_path):
    """Open a CSV file in Pandas."""
    return pd.read_csv(file_path, header=None, dtype=str).fillna("")

def evaluate(student_file, data_solutions, data_assignment):
    """Evaluate the student file and assign a score."""
    student_name, student_surname = [
        part.lower().capitalize() for part in 
        os.path.splitext(os.path.basename(student_file))[0].split('-')
    ]
    data_student = read(student_file)
    
    score = 0
    total_cells = 0
    
    for i in range(min(len(data_solutions), len(data_student))):
        for j in range(min(len(data_solutions.columns), len(data_student.columns))):
            
            if data_solutions.iat[i, j] != data_assignment.iat[i, j]:  # Check the difference cells
                total_cells += 1
                
                if data_solutions.iat[i, j] == data_student.iat[i, j]:
                    score += 1
    
    percentage = (score / total_cells) * 100 if total_cells > 0 else 0
    return student_name, student_surname, round(percentage, 2)

def main():
    """Evaluate student files for an input assignment."""
    assignment = sys.argv[1] if len(sys.argv) > 1 else None
    
    assignments_path = "assignments"
    solutions_path = "solutions"
    
    if not assignment:
        assignment = os.path.basename(get(assignments_path))
    
    if not assignment:
        print("Error: Assignment not available.")
        return
    
    assignment_folder = os.path.join(assignments_path, assignment)
    solution_file = os.path.join(solutions_path, assignment, "solution.csv")
    assignment_file = os.path.join(solutions_path, assignment, "assignment.csv")

    output_folder = "evaluations"
    os.makedirs(output_folder, exist_ok=True)

    report_file = os.path.join(output_folder, f"{assignment}-Report.csv")
    
    if not os.path.exists(assignment_folder):
        print(f"Error: Folder '{assignment_folder}' not available.")
        return
    
    if not os.path.exists(solution_file):
        print(f"Error: File '{solution_file}' not available.")
        return
    
    if not os.path.exists(assignment_file):
        print(f"Error: File '{assignment_file}' not available.")
        return
    
    data_solutions = read(solution_file)
    data_assignment = read(assignment_file)
    
    results = []
    
    for file in os.listdir(assignment_folder):
        if file.endswith(".csv"):
            student_file = os.path.join(assignment_folder, file)
            student_name, student_surname, score = evaluate(student_file, data_solutions, data_assignment)
            
            results.append({"Name": student_name, "Surname": student_surname, "Score (%)": score})
            print(f"Assessment {file}: {score}%")
    
    data_report = pd.DataFrame(results)
    data_report.to_csv(report_file, index=False)
    print(f"Evaluation Report: {report_file}")

if __name__ == "__main__":
    main()
