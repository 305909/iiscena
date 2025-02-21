import os
import sys
import pandas as pd


class CsvFileHandler:
    """
    A class for handling CSV file reading and directory operations related to assignment evaluations.

    This class provides static methods to:
      - Retrieve the most recently modified folder in a given directory.
      - Read CSV files into a pandas DataFrame with specific settings.
    """

    @staticmethod
    def get_latest_folder(directory_path: str) -> str:
        """
        Retrieve the most recently modified subdirectory in the specified directory.

        This method iterates over all entries in the given directory and identifies
        which subdirectory was modified last based on the modification time.

        :param directory_path: Path to the directory containing subdirectories.
        :return: The path of the latest subdirectory, or None if no subdirectories exist.
        """
        subdirectories = [
            os.path.join(directory_path, entry)
            for entry in os.listdir(directory_path)
            if os.path.isdir(os.path.join(directory_path, entry))
        ]
        if not subdirectories:
            return None
        # Use os.path.getmtime to determine the most recently modified folder.
        return max(subdirectories, key=os.path.getmtime)

    @staticmethod
    def read_csv_file(file_path: str) -> pd.DataFrame:
        """
        Read a CSV file using pandas with no header and all columns as strings.

        Missing values are replaced with empty strings.

        :param file_path: The file path of the CSV file.
        :return: A pandas DataFrame containing the CSV data.
        """
        return pd.read_csv(file_path, header=None, dtype=str).fillna("")


class StudentEvaluator:
    """
    A class to evaluate a student's CSV submission against the solution and assignment data.

    This class extracts the student's name from the file name (expected in the format 'name-surname.csv')
    and computes a score by comparing the student's answers cell-by-cell with the solution, but only in cells
    where the solution differs from the assignment template. Additionally, it generates a detailed Markdown
    report of the comparisons.
    """

    @staticmethod
    def evaluate_student_file(
        student_file: str, solution_data: pd.DataFrame, assignment_data: pd.DataFrame
    ) -> tuple[str, str, float, str]:
        """
        Evaluate a student's CSV file and compute a score based on cell-by-cell comparison.

        The method:
          - Extracts the student's first name and surname from the file name.
          - Reads the student's CSV file.
          - Iterates through each cell within the minimum overlapping range of the solution and student data.
          - Considers only cells where the solution differs from the assignment data.
          - Increments the score if the student's value matches the solution.
          - Appends detailed comparison results for each evaluated cell.
          - Computes the percentage score of correctly answered cells.

        :param student_file: Path to the student's CSV file.
        :param solution_data: DataFrame containing the correct solution values.
        :param assignment_data: DataFrame containing the assignment baseline values.
        :return: A tuple containing:
                 - The student's first name (capitalized).
                 - The student's surname (capitalized).
                 - The computed score percentage rounded to two decimal places.
                 - A detailed Markdown formatted report (string) of the comparisons.
        """
        # Extract the student's first and last names from the file name.
        base_name = os.path.splitext(os.path.basename(student_file))[0]
        name_parts = base_name.split('-')
        student_first_name, student_last_name = [
            part.lower().capitalize() for part in name_parts
        ]

        # Read the student's CSV submission.
        student_data = CsvFileHandler.read_csv_file(student_file)

        score = 0
        total_evaluated_cells = 0
        detailed_report_lines = []
        detailed_report_lines.append(f"# Detailed Comparison Report for {student_first_name} {student_last_name}\n")
        detailed_report_lines.append("This report details each cell comparison where the solution differs from the assignment baseline.\n")

        # Determine the common range to compare based on both data dimensions.
        rows_to_compare = min(len(solution_data), len(student_data))
        cols_to_compare = min(len(solution_data.columns), len(student_data.columns))

        # Iterate over each cell in the overlapping region.
        for i in range(rows_to_compare):
            for j in range(cols_to_compare):
                sol_value = solution_data.iat[i, j]
                assign_value = assignment_data.iat[i, j]
                student_value = student_data.iat[i, j]
                # Evaluate only cells where the solution differs from the assignment template.
                if sol_value != assign_value:
                    total_evaluated_cells += 1
                    if sol_value == student_value:
                        score += 1
                        result = "Correct"
                    else:
                        result = "Incorrect"
                    detailed_report_lines.append(
                        f"- **Cell ({i+1}, {j+1})**: Expected: `{sol_value}`, Student: `{student_value}` → **{result}**"
                    )

        # Calculate the percentage score, handling the case with zero evaluated cells.
        percentage = (score / total_evaluated_cells) * 100 if total_evaluated_cells > 0 else 0
        detailed_report_lines.append(f"\n**Total Evaluated Cells**: {total_evaluated_cells}")
        detailed_report_lines.append(f"**Correct Answers**: {score}")
        detailed_report_lines.append(f"**Final Score**: {round(percentage, 2)}%")

        detailed_report = "\n".join(detailed_report_lines)
        return student_first_name, student_last_name, round(percentage, 2), detailed_report


class AssignmentEvaluator:
    """
    A class to manage the evaluation of student CSV submissions for an assignment.

    This class handles:
      - Determining the assignment folder either via command-line argument or by selecting
        the most recently modified folder.
      - Validating the existence of required directories and CSV files.
      - Evaluating all student CSV submissions within the assignment folder.
      - Generating a consolidated CSV report of the evaluation results.
      - Generating an individual Markdown report for each student.
    """

    def __init__(self, assignment_arg: str = None):
        """
        Initialize the AssignmentEvaluator with an assignment identifier.

        :param assignment_arg: The assignment identifier from the command-line (optional).
        """
        self.assignments_directory = "assignments"
        self.solutions_directory = "solutions"
        self.evaluations_directory = "evaluations"
        self.assignment = assignment_arg

        # If no assignment argument is provided, retrieve the latest assignment folder.
        if not self.assignment:
            latest_folder = CsvFileHandler.get_latest_folder(self.assignments_directory)
            if latest_folder:
                self.assignment = os.path.basename(latest_folder)

        # Construct paths for the assignment folder, solution file, assignment template file, and report.
        self.assignment_folder = os.path.join(self.assignments_directory, self.assignment) \
            if self.assignment else None
        self.solution_file = os.path.join(
            self.solutions_directory, self.assignment, "solution.csv"
        ) if self.assignment else None
        self.assignment_file = os.path.join(
            self.solutions_directory, self.assignment, "assignment.csv"
        ) if self.assignment else None
        self.report_file = os.path.join(
            self.evaluations_directory, f"{self.assignment}-Report.csv"
        ) if self.assignment else None

    def verify_resources(self) -> bool:
        """
        Verify that all necessary folders and files exist for the evaluation process.

        The method checks for the existence of:
          - The assignment folder.
          - The solution CSV file.
          - The assignment template CSV file.

        :return: True if all required resources are available; otherwise, prints an error and returns False.
        """
        if not self.assignment:
            print("Error: Assignment not available.")
            return False

        if not os.path.exists(self.assignment_folder):
            print(f"Error: Folder '{self.assignment_folder}' not available.")
            return False

        if not os.path.exists(self.solution_file):
            print(f"Error: File '{self.solution_file}' not available.")
            return False

        if not os.path.exists(self.assignment_file):
            print(f"Error: File '{self.assignment_file}' not available.")
            return False

        return True

    def run_evaluation(self) -> None:
        """
        Execute the evaluation process for all student CSV submissions in the assignment folder.

        The process includes:
          - Verifying resource availability.
          - Reading the solution and assignment CSV files.
          - Iterating through each student CSV file in the assignment folder.
          - Evaluating each student's submission and printing individual results.
          - Generating a consolidated CSV report of all evaluations.
          - Generating an individual Markdown report for each student with detailed comparisons.
        """
        # Validate that all required files and directories exist.
        if not self.verify_resources():
            return

        # Ensure the evaluations output directory exists.
        os.makedirs(self.evaluations_directory, exist_ok=True)

        # Read the solution and assignment CSV files.
        solution_data = CsvFileHandler.read_csv_file(self.solution_file)
        assignment_data = CsvFileHandler.read_csv_file(self.assignment_file)

        evaluation_results = []

        # Process each CSV file found in the assignment folder.
        for file in os.listdir(self.assignment_folder):
            if file.endswith(".csv"):
                student_file_path = os.path.join(self.assignment_folder, file)
                # Evaluate the student's file, obtaining both the score and detailed report.
                first_name, last_name, score, detailed_report = StudentEvaluator.evaluate_student_file(
                    student_file_path, solution_data, assignment_data
                )
                evaluation_results.append({
                    "Name": first_name,
                    "Surname": last_name,
                    "Score (%)": score
                })
                print(f"Assessment {file}: {score}%")

                # Generate an individual Markdown report for the student.
                individual_report_filename = f"{self.assignment}-{first_name}-{last_name}-Report.md"
                individual_report_path = os.path.join(self.evaluations_directory, individual_report_filename)
                with open(individual_report_path, "w", encoding="utf-8") as md_file:
                    md_file.write(detailed_report)
                print(f"Detailed report generated for {file}: {individual_report_path}")

        # Convert the evaluation results into a DataFrame and save as a CSV report.
        report_dataframe = pd.DataFrame(evaluation_results)
        report_dataframe.to_csv(self.report_file, index=False)
        print(f"Consolidated Evaluation Report generated at: {self.report_file}")


def main():
    """
    Main function to evaluate student CSV submissions for an assignment.

    The assignment identifier is taken from the command-line arguments if provided.
    Otherwise, the most recent assignment folder is used.
    """
    # Retrieve assignment identifier from command-line arguments (if available).
    assignment_identifier = sys.argv[1] if len(sys.argv) > 1 else None

    # Initialize the AssignmentEvaluator with the provided assignment identifier.
    evaluator = AssignmentEvaluator(assignment_identifier)
    evaluator.run_evaluation()


if __name__ == "__main__":
    main()
