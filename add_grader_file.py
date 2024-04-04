import os
import shutil

# Define source and destination directories
directory = "A9_student_files"
grader_file = "grader.py"

# Traverse through source directory
for student_id in os.listdir(directory):
    student_dest_dir = os.path.join(directory, student_id)
    if os.path.isdir(student_dest_dir):
        shutil.copy(grader_file, student_dest_dir)

print("Copying grader.py complete.")