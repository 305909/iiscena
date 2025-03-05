#!/usr/bin/env python3
"""
CSV/ODS Assignment Evaluator for the OpenOffice Calc Course at "I.I.S. G. Cena di Ivrea".

Author: Francesco Giuseppe Gillio
Date: 25.02.2025
"""

import os
import sys
import json
import subprocess
import pandas as pd


def _get_class_register(registry_path: str) -> dict:
  
    try:
        with open(registry_path, "r") as file:
            registry = json.load(file)
            return registry
    except Exception as e:
        print(f"Unable to load registry {registry_path}: {e}")
        sys.exit(1)


def _get_csv(ods_file_path: str) -> str:

    if not ods_file_path.lower().endswith(".ods"):
        return ods_file_path
    csv_file_path = ods_file_path.rsplit('.', 1)[0] + '.csv'
    try:
        subprocess.run(
            [
                'libreoffice', 
                '--headless', 
                '--convert-to', 
                'csv',
                ods_file_path, 
                '--outdir', 
                os.path.dirname(ods_file_path)
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return csv_file_path
    except Exception as e:
        print(f"Unable to convert ODS file {ods_file_path}: {e}")
        return ods_file_path


class CsvFileHandler:

    @staticmethod
    def _read_csv(csv_file_path: str) -> pd.DataFrame:

        return pd.read_csv(csv_file_path, header=None, dtype=str).fillna("")


class StudentEvaluator:

    @staticmethod
    def _evaluate_submission(
        student_file_path: str,
        student_name: str,
        solution_data: pd.DataFrame,
        assignment_data: pd.DataFrame
    ) -> tuple[float, str]:

        student_data = CsvFileHandler._read_csv(student_file_path)

        score = 0
        total_cells_evaluated = 0
        errors = []

        rows_to_evaluate = min(len(solution_data), len(student_data))
        cols_to_evaluate = min(len(solution_data.columns), len(student_data.columns))

        for row_idx in range(rows_to_evaluate):
            for col_idx in range(cols_to_evaluate):
                solution_value = solution_data.iat[row_idx, col_idx]
                assignment_value = assignment_data.iat[row_idx, col_idx]
                student_value = student_data.iat[row_idx, col_idx]

                if solution_value != assignment_value:
                    total_cells_evaluated += 1
                    if solution_value == student_value:
                        score += 1
                    else:
                        errors.append(f"- **Cell ({row_idx + 1}, {col_idx + 1}) mismatch:**")
                        errors.append(f"  - **Result:** `{solution_value}`")
                        errors.append(f"  - **Student Submission:** `{student_value}`")

        score_percentage = (score / total_cells_evaluated) * 100 if total_cells_evaluated > 0 else 0

        report_lines = []
        report_lines.append(f"# Evaluation Report for {student_name}\n")
        report_lines.append("## Overview\n")
        report_lines.append(f"- **Total Cells:** {total_cells_evaluated}")
        report_lines.append(f"- **Correct Answers:** {score}")
        report_lines.append(f"- **Final Score:** {round(score_percentage, 2)}%\n")
        report_lines.append("## Errors\n")
        if errors:
            report_lines.extend(errors)
        else:
            report_lines.append("- No errors.")

        detailed_report = "\n".join(report_lines)
        return round(score_percentage, 2), detailed_report


class AssignmentEvaluator:

    def __init__(self, assignment_id: str, registry_file_path: str):

        self.assignment_directory = "assignments"
        self.solutions_directory = "solutions"
        self.evaluations_directory = "evaluations"
        self.assignment_id = assignment_id
        self.student_registry = _get_class_register(registry_file_path)

        if not self.assignment_id:
            print("Error: Assignment identifier is mandatory.")
            sys.exit(1)

        self.assignment_folder = os.path.join(self.assignment_directory, *self.assignment_id.split("/"))
        self.evaluation_subfolder = os.path.join(self.evaluations_directory, self.assignment_id)
        os.makedirs(self.evaluation_subfolder, exist_ok=True)

        self.solution_file = self._get_solution_file()
        self.assignment_file = self._get_assignment_template_file()

        self.report_file_path = os.path.join(self.evaluation_subfolder, "REPORT.csv")

    def _get_solution_file(self) -> str:

        solution_path_ods = os.path.join(self.solutions_directory, *self.assignment_id.split("/"), "solution.ods")
        solution_path_csv = os.path.join(self.solutions_directory, *self.assignment_id.split("/"), "solution.csv")

        if os.path.exists(solution_path_ods):
            return _get_csv(solution_path_ods)
        elif os.path.exists(solution_path_csv):
            return solution_path_csv
        else:
            print(f"Error: Solution file for '{self.assignment_id}' is not available.")
            sys.exit(1)

    def _get_assignment_template_file(self) -> str:

        assignment_path_ods = os.path.join(self.solutions_directory, *self.assignment_id.split("/"), "assignment.ods")
        assignment_path_csv = os.path.join(self.solutions_directory, *self.assignment_id.split("/"), "assignment.csv")

        if os.path.exists(assignment_path_ods):
            return _get_csv(assignment_path_ods)
        elif os.path.exists(assignment_path_csv):
            return assignment_path_csv
        else:
            print(f"Error: Assignment template file for '{self.assignment_id}' is not available.")
            sys.exit(1)

    def _verify_resources(self) -> bool:

        if not os.path.exists(self.assignment_folder):
            print(f"Error: Folder '{self.assignment_folder}' is not available.")
            return False

        if not os.path.exists(self.solution_file):
            print(f"Error: Solution file '{self.solution_file}' is not available.")
            return False

        if not os.path.exists(self.assignment_file):
            print(f"Error: Assignment template file '{self.assignment_file}' is not available.")
            return False

        return True

    def _run_evaluation(self) -> None:

        if not self._verify_resources():
            return

        solution_data = CsvFileHandler._read_csv(self.solution_file)
        assignment_data = CsvFileHandler._read_csv(self.assignment_file)

        evaluation_results = []
        for student_id, student_name in self.student_registry.items():
            student_file = self._get_student_submission(student_name)

            if student_file:
                student_file_path = os.path.join(self.assignment_folder, student_file)
                if student_file_path.lower().endswith(".ods"):
                    student_file_path = _get_csv(student_file_path)

                try:
                    score, report = StudentEvaluator._evaluate_submission(
                        student_file_path, student_name, solution_data, assignment_data
                    )
                    print(f"Evaluation for {student_name}: {score}%")
                except Exception as e:
                    print(f"Execution error for {student_file}: {e}")
                    continue

                evaluation_results.append({
                    "Student": student_name,
                    "Score (%)": score
                })

                self._save_report(student_name, report)
            else:
                print(f"No submission for {student_name}.")
                evaluation_results.append({
                    "Student": student_name,
                    "Score (%)": 0.0
                })
                self._save_report(student_name, f"# Evaluation Report for {student_name}\n\nNo submission, score: 0%\n")

        self._write_report(evaluation_results)

    def _get_student_submission(self, student_name: str) -> str:

        surname = student_name.split()[0].upper()
        for file in os.listdir(self.assignment_folder):
            if file.endswith(".csv") or file.endswith(".ods"):
                if os.path.splitext(os.path.basename(file))[0].upper() == surname:
                    print(f"Submission for {student_name}: {file}")
                    return file
        return None

    def _save_report(self, student_name: str, report: str) -> None:

        individual_report_path = os.path.join(self.evaluation_subfolder, f"{student_name}.md")
        try:
            with open(individual_report_path, "w") as report_file:
                report_file.write(report)
        except Exception as e:
            print(f"Unable to write .MD report for {student_name}: {e}")

    def _write_report(self, evaluation_results: list) -> None:

        report_df = pd.DataFrame(sorted(evaluation_results, key=lambda x: x["Student"]))
        report_df.to_csv(self.report_file_path, index=False)
        print(f"Overall Evaluation Report available at: {self.report_file_path}")


def main():

    if len(sys.argv) < 3:
        print("Error: Please provide the assignment identifier and the registry file path as input parameters.")
        return

    assignment_id = sys.argv[1]
    registry_file_path = sys.argv[2]

    evaluator = AssignmentEvaluator(assignment_id, registry_file_path)
    evaluator._run_evaluation()


if __name__ == "__main__":
    main()
