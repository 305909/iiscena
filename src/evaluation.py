import os
import uno
import pandas as pd

# Configuration: Paths for solution file and student submissions
SOLUTIONS_FILE = "solutions/solution.ods"  # File with the correct answers
ASSIGNMENTS_FOLDER = "homework/"  # Folder with student submissions
REPORT_FILE = "report.csv"  # Output file with student scores

# Connect to LibreOffice/OpenOffice
local_context = uno.getComponentContext()
resolver = local_context.ServiceManager.createInstanceWithContext(
    "com.sun.star.bridge.UnoUrlResolver", local_context
)
ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)

def open_calc_file(path):
    """Opens an ODS file in LibreOffice."""
    url = uno.systemPathToFileUrl(os.path.abspath(path))
    return desktop.loadComponentFromURL(url, "_blank", 0, ())

def read_sheet_data(document):
    """Extracts data from an OpenOffice Calc sheet and returns a DataFrame."""
    sheet = document.Sheets.getByIndex(0)  # Use the first sheet
    data = []
    
    for row in range(1, 50):  # Assume max 50 rows
        row_data = []
        for col in range(1, 20):  # Assume max 20 columns
            cell = sheet.getCellByPosition(col, row)
            value = cell.getFormula() if cell.Formula else cell.getValue()
            row_data.append(value)
        data.append(row_data)
    
    return pd.DataFrame(data)

def evaluate_submission(student_file, data_solutions):
    """Compares a student's file with the solution file and assigns a score."""
    student_doc = open_calc_file(student_file)
    data_student = read_sheet_data(student_doc)

    score = 0
    total_cells = data_solutions.size

    for (i, j), solution_value in data_solutions.stack().items():
        student_value = data_student.at[i, j] if (i, j) in data_student.index else None
        if student_value == solution_value:
            score += 1  # Points for each correct cell

    percentage = (score / total_cells) * 100
    return round(percentage, 2)

def main():
    """Iterates through student files, evaluates them, and generates a report."""
    if not os.path.exists(ASSIGNMENTS_FOLDER):
        print(f"Error: folder '{ASSIGNMENTS_FOLDER}' not available.")
        return

    solution_doc = open_calc_file(SOLUTIONS_FILE)
    data_solutions = read_sheet_data(solution_doc)
  
    results = []
  
    for file in os.listdir(ASSIGNMENTS_FOLDER):
        if file.endswith(".ods"):
            file_path = os.path.join(ASSIGNMENTS_FOLDER, file)
            score = evaluate_submission(file_path, data_solutions)
            results.append({"Student": file, "Score (%)": score})
            print(f"Evaluating {file}: {score}%")

    data_report = pd.DataFrame(results)
    data_report.to_csv(REPORT_FILE, index=False)
    print(f"Report: {REPORT_FILE}")

if __name__ == "__main__":
    main()
