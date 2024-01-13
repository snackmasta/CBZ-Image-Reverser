import os
import sys
import uuid
import zipfile
import tempfile
import shutil
import argparse

from PIL import Image

# Create the parser
parser = argparse.ArgumentParser(description='Process a CBZ file.')
parser.add_argument('cbz_file', type=str, help='The CBZ file to process')
parser.add_argument('--reverse', action='store_true', help='Reverse the order of files')
parser.add_argument('--swap', action='store_true', help='Swap the order of files in pairs')

# Parse the arguments
args = parser.parse_args()

def process_cbz_file(cbz_file, args):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(cbz_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Process the CBZ file
        if args.reverse:
            reverse_file_order(temp_dir)
        elif args.swap:
            swap_page_pair(temp_dir)
        else:
            print("Please specify either --reverse or --swap")
        
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

def reverse_file_order(directory):
    # Create a list of files in the directory
    files = os.listdir(directory)
    
    # Iterate over the list of files in steps of 1
    for i in range(0, len(files), 1):
        if i + 1 <= len(files)/2:
            file_count = len(files)
            temp = os.path.join(directory, str(uuid.uuid4()))
            file1 = os.path.join(directory, files[i])
            file2 = os.path.join(directory, files[file_count - i - 1])
            try:
                os.rename(file1, temp)
                os.rename(file2, file1)
                os.rename(temp, file2)
            except Exception as e:
                print(f"Error swapping files {files[i]} and {files[i+1]}: {e}")

# Check if the script is called with the correct number of arguments
if len(sys.argv) != 3:
    print("Usage: python script.py <cbz_file>")
else:
    # Process the CBZ file
    process_cbz_file(args.cbz_file, args)