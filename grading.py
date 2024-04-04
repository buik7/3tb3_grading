import os
import subprocess

# Define source directory
source_dir = "A9_student_files"
feedback_file = "A9_feedback.txt"

# Function to run grader.py in each student folder and capture the output
def run_grader(student_dir, feedback_file):
    grader_script = os.path.join(student_dir, "grader.py")
    if os.path.exists(grader_script):
        process = subprocess.Popen(['python', grader_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        with open(feedback_file, 'a', encoding='utf-8') as f:
            f.write(f"MacID: {os.path.basename(student_dir)}\n\n")
            f.write(stdout.decode('utf-8'))
            if stderr:
                f.write(stderr.decode('utf-8'))
            f.write("\n\n\n")

# Run grader in each student folder and append feedback to A9_feedback.txt
for student_id in os.listdir(source_dir):
    student_folder = os.path.join(source_dir, student_id)
    if os.path.isdir(student_folder):
        run_grader(student_folder, feedback_file)

print("Grading and combining feedback complete.")