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
        
        # # Print the list of files in the temporary directory
        # print("Files in temporary directory:")
        # for root, dirs, files in os.walk(temp_dir):
        #     for file in files:
        #         print(file)
        
        # Reverse the order of files in the temporary directory
        reverse_file_order(temp_dir)
        
        with zipfile.ZipFile(cbz_file, 'w') as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    # Write the files back to the zip file
                    zipf.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), temp_dir))

def reverse_file_order(directory):
    # Create a list of files in the directory
    files = os.listdir(directory)
    
    # Iterate over the list of files in steps of 1
    for i in range(0, len(files), 1):
        # Check if the next file exists
        if i + 1 <= len(files)+1:
            # Get the total number of files
            file_count = len(files)
            # Create a temporary file name using a random UUID
            temp = os.path.join(directory, str(uuid.uuid4()))
            # Get the full path of the current file
            file1 = os.path.join(directory, files[i])
            # Get the full path of the next file
            file2 = os.path.join(directory, files[file_count - i - 1])
            print(f"Swapping files {files[i]} and {files[file_count - i - 1]}")
            # print(f"Swapping files {files[i]}")
            try:
                # Rename the current file to the temporary file
                os.rename(file1, temp)
                # Rename the next file to the current file
                os.rename(file2, file1)
                # Rename the temporary file to the next file
                os.rename(temp, file2)
            except Exception as e:
                # Print an error message if an exception occurs during the file swapping
                print(f"Error swapping files {files[i]} and {files[i+1]}: {e}")

# Check if the script is called with the correct number of arguments
if len(sys.argv) != 2:
    print("Usage: python script.py <cbz_file>")
else:
    # Process the CBZ file
    process_cbz_file(sys.argv[1])