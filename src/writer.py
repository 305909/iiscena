import os
import sys
import pandas as pd
from docx import Document

def get_margins(doc):
    """Ottiene i margini del documento DOCX (in cm)."""
    section = doc.sections[0]
    return {
        "top": section.top_margin.cm,
        "bottom": section.bottom_margin.cm,
        "left": section.left_margin.cm,
        "right": section.right_margin.cm,
    }

def get_paragraph_styles(doc):
    """Ottiene le proprietà di formattazione dei paragrafi."""
    styles = []
    for para in doc.paragraphs:
        styles.append({
            "text": para.text,
            "alignment": para.alignment,
            "font_name": para.runs[0].font.name if para.runs else "",
            "font_size": para.runs[0].font.size.pt if para.runs and para.runs[0].font.size else "",
            "space_before": para.paragraph_format.space_before.pt if para.paragraph_format.space_before else "",
            "space_after": para.paragraph_format.space_after.pt if para.paragraph_format.space_after else "",
        })
    return styles

def evaluate_submission(student_file, solution_doc):
    """Valuta il documento dello studente confrontandolo con il file soluzione."""
    student_name, student_surname = os.path.splitext(os.path.basename(student_file))[0].split('-')
    student_doc = Document(student_file)
    
    score = 0
    total_checks = 0
    
    # Valuta i margini
    student_margins = get_margins(student_doc)
    solution_margins = get_margins(solution_doc)
    for key in student_margins:
        total_checks += 1
        if student_margins[key] == solution_margins[key]:
            score += 1
    
    # Valuta la formattazione dei paragrafi
    student_styles = get_paragraph_styles(student_doc)
    solution_styles = get_paragraph_styles(solution_doc)
    for i in range(min(len(student_styles), len(solution_styles))):
        total_checks += 5  # Cinque controlli per paragrafo (allineamento, font, dimensione, spazio prima, spazio dopo)
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
    """Valuta i file degli studenti per una specifica lezione."""
    if len(sys.argv) < 2:
        print("Errore: Specificare il nome della sottocartella delle assegnazioni.")
        return
    
    lesson_name = sys.argv[1]
    assignments_path = "assignments"
    solutions_path = "solutions"
    evaluations_path = "evaluations"
    
    assignment_folder = os.path.join(assignments_path, lesson_name)
    solution_file = os.path.join(solutions_path, lesson_name, "solution.docx")
    report_file = os.path.join(evaluations_path, f"{lesson_name}-report.csv")
    
    if not os.path.exists(assignment_folder):
        print(f"Errore: Cartella '{assignment_folder}' non trovata.")
        return
    
    if not os.path.exists(solution_file):
        print(f"Errore: File '{solution_file}' non trovato.")
        return
    
    if not os.path.exists(evaluations_path):
        os.makedirs(evaluations_path)
    
    solution_doc = Document(solution_file)
    results = []
    
    for file in os.listdir(assignment_folder):
        if file.endswith(".docx"):
            student_file = os.path.join(assignment_folder, file)
            student_name, student_surname, score = evaluate_submission(student_file, solution_doc)
            results.append({"Name": student_name, "Surname": student_surname, "Score (%)": score})
            print(f"Valutazione {file}: {score}%")
    
    data_report = pd.DataFrame(results)
    data_report.to_csv(report_file, index=False)
    print(f"Report generato: {report_file}")

if __name__ == "__main__":
    main()
