import os
import shutil
from datetime import datetime, timedelta

# Define the root directory to search and the destination directory
root_dir = 'MinMax/PNG_Out/Napkon/'  # Replace with your source directory
dest_dir = 'MinMax/PNG_Out/Trash/'  # Replace with your destination directory

# Define the time threshold (36 hours ago)
time_threshold = datetime.now() - timedelta(hours=40)

# Walk through all subdirectories
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.png'):
            full_path = os.path.join(subdir, file)
            
            # Get the file's last modification time
            file_mtime = datetime.fromtimestamp(os.path.getmtime(full_path))
            
            # Check if the file is older than 40 hours
            if file_mtime < time_threshold:
                # Calculate the relative path and destination path
                relative_path = os.path.relpath(full_path, root_dir)
                dest_path = os.path.join(dest_dir, relative_path)
                
                # Create destination directories if they don't exist
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Move the file to the destination directory
                shutil.move(full_path, dest_path)

print("Files moved successfully.")