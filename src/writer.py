import os
import sys
import pandas as pd

from docx import Document

def get_margins(doc):
    """Gets the margins of the DOCX document (in cm)."""
    section = doc.sections[0]
    return {
        "top": section.top_margin.cm,
        "bottom": section.bottom_margin.cm,
        "left": section.left_margin.cm,
        "right": section.right_margin.cm,
    }

def get_styles(doc):
    """Gets the format properties of paragraphs."""
    styles = []
    for para in doc.paragraphs:
        styles.append({
            "text": 
            para.text,
            "alignment": 
            para.alignment,
            "font_name": 
            para.runs[0].font.name if para.runs else "",
            "font_size": 
            para.runs[0].font.size.pt if para.runs and para.runs[0].font.size else "",
            "space_before": 
            para.paragraph_format.space_before.pt if para.paragraph_format.space_before else "",
            "space_after": 
            para.paragraph_format.space_after.pt if para.paragraph_format.space_after else "",
        })
    return styles

def evaluate(student_file, solution_doc):
    """Evaluate the student file and assign a score."""
    student_name, student_surname = [
        part.lower().capitalize() for part in 
        os.path.splitext(os.path.basename(student_file))[0].split('-')
    ]
    student_doc = Document(student_file)
    
    score = 0
    total_checks = 0
    
    # Evaluate the margins
    student_margins = get_margins(student_doc)
    solution_margins = get_margins(solution_doc)
    for key in student_margins:
        total_checks += 1
        if student_margins[key] == solution_margins[key]:
            score += 1
    
    # Evaluate the format properties of paragraphs
    student_styles = get_styles(student_doc)
    solution_styles = get_styles(solution_doc)
    for i in range(min(len(student_styles), len(solution_styles))):
        total_checks += 5  # Five controls per paragraph (alignment, font, size, space before, space after)
        if student_styles[i]["alignment"] == solution_styles[i]["alignment"]:
            score += 1
        if student_styles[i]["font_name"] == solution_styles[i]["font_name"]:
            score += 1
        if student_styles[i]["font_size"] == solution_styles[i]["font_size"]:
            score += 1
        if student_styles[i]["space_before"] == solution_styles[i]["space_before"]:
            score += 1
        if student_styles[i]["space_after"] == solution_styles[i]["space_after"]:
            score += 1
    
    percentage = (score / total_checks) * 100 if total_checks > 0 else 0
    return student_name, student_surname, round(percentage, 2)

def main():

    """Evaluate student files for an input assignment."""
    assignment = sys.argv[1] if len(sys.argv) > 1 else None
    
    assignments_path = "assignments"
    solutions_path = "solutions"
    
    if not assignment:
        print("Error: Assignment not available.")
        return
    
    assignment_folder = os.path.join(assignments_path, assignment)
    solution_file = os.path.join(solutions_path, assignment, "solution.docx")
    
    output_folder = "evaluations"
    os.makedirs(output_folder, exist_ok=True)

    report_file = os.path.join(output_folder, f"{assignment}-Report.csv")

    if not os.path.exists(assignment_folder):
        print(f"Error: Folder '{assignment_folder}' not available.")
        return
    
    if not os.path.exists(solution_file):
        print(f"Error: File '{solution_file}' not available.")
        return
    
    solution_doc = Document(solution_file)

    results = []
    
    for file in os.listdir(assignment_folder):
        if file.endswith(".docx"):
            student_file = os.path.join(assignment_folder, file)
            student_name, student_surname, score = evaluate(student_file, solution_doc)
            
            results.append({"Name": student_name, "Surname": student_surname, "Score (%)": score})
            print(f"Assessment {file}: {score}%")
    
    data_report = pd.DataFrame(results)
    data_report.to_csv(report_file, index=False)
    print(f"Evaluation Report: {report_file}")

if __name__ == "__main__":
    main()
