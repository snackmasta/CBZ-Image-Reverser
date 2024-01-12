import os
import sys
import uuid
import zipfile
import tempfile
import shutil

from PIL import Image

def reverse_file_order(directory):
    # Get a list of files in the directory with width less than or equal to height
    files = [f for f in os.listdir(directory) if Image.open(os.path.join(directory, f)).size[0] <= Image.open(os.path.join(directory, f)).size[1]]
    
    # Sort the files in ascending order
    files.sort()

    # Reverse the list of files
    files.reverse()

    temp_files = []
    try:
        # Rename each file to a temporary name
        for f in files:
            temp = os.path.join(directory, str(uuid.uuid4()))
            shutil.move(os.path.join(directory, f), temp)
            temp_files.append(temp)

        # Rename each temporary file to its new name in the reversed order
        for i, temp in enumerate(temp_files):
            shutil.move(temp, os.path.join(directory, files[i]))
    except Exception as e:
        print(f"Error reversing file order: {e}")

def process_cbz_file(cbz_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(cbz_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        with zipfile.ZipFile(cbz_file, 'w') as zipf:
            # Get the list of all files in the directory
            files = [os.path.join(root, file) for root, dirs, files in os.walk(temp_dir) for file in files]
            
            # Sort the list of files in reverse order
            files.sort(reverse=True)
            
            # Add each file to the .cbz file
            for file in files:
                zipf.write(file, arcname=os.path.relpath(file, temp_dir))

# Check if the script is called with the correct number of arguments
if len(sys.argv) != 2:
    print("Usage: python script.py <cbz_file>")
else:
    # Process the CBZ file
    process_cbz_file(sys.argv[1])