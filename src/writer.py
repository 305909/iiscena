import os
import sys
import pandas as pd
from docx import Document
import difflib

def get_margins(doc):
    """Gets the margins of the DOCX document (in cm)."""
    section = doc.sections[0]
    return {
        "top": section.top_margin.cm,
        "bottom": section.bottom_margin.cm,
        "left": section.left_margin.cm,
        "right": section.right_margin.cm,
    }

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
    sequence_matcher = difflib.SequenceMatcher(None, student_text, solution_text)
    match_ratio = sequence_matcher.ratio()
    return round(match_ratio * 5, 2)

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
    
    print(f"Margins for {student_name} {student_surname}:")
    for key in student_margins:
        print(f"  {key.capitalize()} margin - Solution: {solution_margins[key]} cm, Student: {student_margins[key]} cm", end="")
        if student_margins[key] == solution_margins[key]:
            print(" | Punteggio: 1/1")
            score += 1
        else:
            print(" | Punteggio: 0/1")
        total_checks += 1
    
    # Evaluate the format properties line by line
    student_lines = get_lines(student_doc)
    solution_lines = get_lines(solution_doc)
    
    print(f"\nEvaluating formatting and content for {student_name} {student_surname}:")
    
    for i in range(min(len(student_lines), len(solution_lines))):
        print(f"Line {i+1}:")
        
        # Format properties
        format_score = 0
        print(f"  Alignment - Solution: {solution_lines[i]['alignment']}, Student: {student_lines[i]['alignment']}", end="")
        if student_lines[i]["alignment"] == solution_lines[i]["alignment"]:
            print(" | Punteggio: 1/1")
            format_score += 1
        else:
            print(" | Punteggio: 0/1")
        
        print(f"  Font Name - Solution: {solution_lines[i]['font_name']}, Student: {student_lines[i]['font_name']}", end="")
        if student_lines[i]["font_name"] == solution_lines[i]["font_name"]:
            print(" | Punteggio: 1/1")
            format_score += 1
        else:
            print(" | Punteggio: 0/1")
        
        print(f"  Font Size - Solution: {solution_lines[i]['font_size']}, Student: {student_lines[i]['font_size']}", end="")
        if student_lines[i]["font_size"] == solution_lines[i]["font_size"]:
            print(" | Punteggio: 1/1")
            format_score += 1
        else:
            print(" | Punteggio: 0/1")
        
        print(f"  Space Before - Solution: {solution_lines[i]['space_before']}, Student: {student_lines[i]['space_before']}", end="")
        if student_lines[i]["space_before"] == solution_lines[i]["space_before"]:
            print(" | Punteggio: 1/1")
            format_score += 1
        else:
            print(" | Punteggio: 0/1")
        
        print(f"  Space After - Solution: {solution_lines[i]['space_after']}, Student: {student_lines[i]['space_after']}", end="")
        if student_lines[i]["space_after"] == solution_lines[i]["space_after"]:
            print(" | Punteggio: 1/1")
            format_score += 1
        else:
            print(" | Punteggio: 0/1")
        
        # Evaluate text content
        text_score = compare_text(student_lines[i]["text"], solution_lines[i]["text"])
        print(f"  Text - Solution: '{solution_lines[i]['text']}', Student: '{student_lines[i]['text']}'", end="")
        print(f" | Text Punteggio: {text_score}/5")
        
        score += format_score + text_score
        total_checks += 5  # Five checks per line
    
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
