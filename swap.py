import os
import sys
import uuid
import zipfile
import tempfile
import shutil

from PIL import Image

def process_cbz_file(cbz_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(cbz_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Reverse the order of files in the temporary directory
        swap_page_pair(temp_dir)
        
        with zipfile.ZipFile(cbz_file, 'w') as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    # Write the files back to the zip file
                    zipf.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), temp_dir))

def swap_page_pair(directory):
    # Get a list of files in the directory with width less than or equal to height
    files = [f for f in os.listdir(directory) if Image.open(os.path.join(directory, f)).size[0] <= Image.open(os.path.join(directory, f)).size[1]]
    
    # Swap the order of files in pairs
    for i in range(0, len(files), 2):
        if i + 1 < len(files):
            temp = os.path.join(directory, str(uuid.uuid4()))
            file1 = os.path.join(directory, files[i])
            file2 = os.path.join(directory, files[i+1])
            try:
                # Swap the files using temporary file
                os.rename(file1, temp)
                os.rename(file2, file1)
                os.rename(temp, file2)
            except Exception as e:
                print(f"Error swapping files {files[i]} and {files[i+1]}: {e}")

# Check if the script is called with the correct number of arguments
if len(sys.argv) != 2:
    print("Usage: python script.py <cbz_file>")
else:
    # Process the CBZ file
    process_cbz_file(sys.argv[1])