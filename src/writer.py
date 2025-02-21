import os
import sys
import pandas as pd
from docx import Document

def get_margins(doc):
    """Gets the margins of the DOCX document (in cm). Handles multiple sections."""
    margins = {}
    for section in doc.sections:
        margins["top"] = section.top_margin.cm
        margins["bottom"] = section.bottom_margin.cm
        margins["left"] = section.left_margin.cm
        margins["right"] = section.right_margin.cm
    return margins

def get_lines(doc):
    """Gets the format properties of each line in the document."""
    lines = []
    for para in doc.paragraphs:
        for run in para.runs:
            lines.append({
                "text": run.text.strip(),
                "alignment": para.alignment,
                "font_name": run.font.name if run.font else "",
                "font_size": run.font.size.pt if run.font and run.font.size else "",
                "space_before": para.paragraph_format.space_before.pt if para.paragraph_format.space_before else "",
                "space_after": para.paragraph_format.space_after.pt if para.paragraph_format.space_after else "",
            })
    return [line for line in lines if line["text"]]

def compare_text(student_text, solution_text):
    """Compares two texts (checks for exact matches with tolerance for case and extra spaces)."""
    student_text = " ".join(student_text.split())
    solution_text = " ".join(solution_text.split())
    
    if student_text.lower() == solution_text.lower():
        return 5  # Perfect match
    
    # More nuanced text comparison (e.g., considering synonym replacement or fuzzy matching)
    # For now, using a simple word-based scoring:
    student_words = set(student_text.split())
    solution_words = set(solution_text.split())
    common_words = student_words.intersection(solution_words)
    return (len(common_words) / len(solution_words)) * 5  # Max score of 5

def compare_format(student_line, solution_line):
    """Compares line formatting properties."""
    score = 0
    total_checks = 5
    
    if student_line["alignment"] == solution_line["alignment"]:
        score += 1
    if student_line["font_name"] == solution_line["font_name"]:
        score += 1
    if student_line["font_size"] == solution_line["font_size"]:
        score += 1
    if student_line["space_before"] == solution_line["space_before"]:
        score += 1
    if student_line["space_after"] == solution_line["space_after"]:
        score += 1
    
    return score, total_checks

def evaluate(student_file, solution_doc):
    """Evaluate the student file and assign a score based on line-by-line formatting and content."""
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
    margin_score = 0
    for key in student_margins:
        total_checks += 1
        if student_margins[key] == solution_margins[key]:
            margin_score += 1
    score += margin_score
    print(f"Margins for {student_name} {student_surname}: {margin_score}/4")

    # Evaluate the format properties line by line
    student_lines = get_lines(student_doc)
    solution_lines = get_lines(solution_doc)
    
    line_score = 0
    for i in range(min(len(student_lines), len(solution_lines))):
        line_format_score, line_format_checks = compare_format(student_lines[i], solution_lines[i])
        line_score += line_format_score
        total_checks += line_format_checks

        # Evaluate text content
        text_score = compare_text(student_lines[i]["text"], solution_lines[i]["text"])
        line_score += text_score
        total_checks += 1  # Add a point for the text comparison

        print(f"Line {i+1}: Format score = {line_format_score}/{line_format_checks}, Text score = {text_score}/5")
    
    score += line_score
    percentage = (score / total_checks) * 100 if total_checks > 0 else 0
    print(f"Final score for {student_name} {student_surname}: {round(percentage, 2)}%")
    
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
            print(f"Assessment {file}: {score}%\n")
    
    data_report = pd.DataFrame(results)
    data_report.to_csv(report_file, index=False)
    
    print(f"Evaluation Report: {report_file}")

if __name__ == "__main__":
    main()
