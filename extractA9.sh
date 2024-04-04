#!/bin/bash

# Set the path to the destination directory
destination_dir="A9submissions"

# Create the destination directory if it doesn't exist
mkdir -p "$destination_dir"

# Loop through each student's directory
for student_dir in submitted/*; do
    student_id=$(basename "$student_dir")
    assignment_dir="$student_dir/Assignment 09"
    
    # Check if the student's directory contains "Assignment 09" folder
    if [ -d "$assignment_dir" ]; then
        # Create the student's directory in the destination directory if it doesn't exist
        mkdir -p "$destination_dir/$student_id"
        
        # Copy the "Assignment 09" folder to the student's directory in the destination directory
        cp -r "$assignment_dir" "$destination_dir/$student_id/"
        echo "Copied 'Assignment 09' folder from $assignment_dir to $destination_dir/$student_id/"
    fi
done

echo "All 'Assignment 09' folders have been copied into respective student ID folders in $destination_dir"
