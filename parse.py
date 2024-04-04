import os
import shutil
import nbformat
from nbconvert import PythonExporter
import re

# Function to convert ipynb to py
def convert_notebook_to_py(notebook_filename, output_filename):
    with open(notebook_filename, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    exporter = PythonExporter()
    source, _ = exporter.from_notebook_node(nb)
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(source)

# Function to remove comments and lines with specified words
def remove_comments_and_lines(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    cleaned_lines = ['import textwrap']
    for line in lines:
        # Remove comments if '#' appears at the beginning of the line only
        line = re.sub(r'^\s*#.*', '', line)
        # Remove lines with 'nbimporter'
        if 'nbimporter' not in line:
            cleaned_lines.append(line)
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

# Define source and destination directories
source_dir = "A9submissions"
destination_dir = "A9_student_files"

# Create destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Traverse through source directory
for student_id in os.listdir(source_dir):
    student_folder = os.path.join(source_dir, student_id, "Assignment 09")
    if os.path.isdir(student_folder):
        # Create student directory in destination folder
        student_dest_dir = os.path.join(destination_dir, student_id)
        os.makedirs(student_dest_dir, exist_ok=True)
        
        # Convert notebooks and copy to student directory
        notebooks = ["P0.ipynb", "ST.ipynb", "CGwat.ipynb", "SC.ipynb", "CGast.ipynb"]
        for notebook in notebooks:
            notebook_path = os.path.join(student_folder, notebook)
            if os.path.exists(notebook_path):
                py_filename = os.path.join(student_dest_dir, notebook.replace(".ipynb", ".py"))
                convert_notebook_to_py(notebook_path, py_filename)
                remove_comments_and_lines(py_filename)

print("Conversion and organization complete.")