import os
import sys
import uuid
import zipfile
import tempfile
import shutil

def reverse_file_order(directory):
    files = os.listdir(directory)
    for i in range(len(files) // 2):
        temp = os.path.join(directory, str(uuid.uuid4()))
        file1 = os.path.join(directory, files[i])
        file2 = os.path.join(directory, files[-i-1])
        try:
            os.rename(file1, temp)
            os.rename(file2, file1)
            os.rename(temp, file2)
        except Exception as e:
            print(f"Error swapping files {files[i]} and {files[-i-1]}: {e}")

def process_cbz_file(cbz_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(cbz_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        reverse_file_order(temp_dir)
        with zipfile.ZipFile(cbz_file, 'w') as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), temp_dir))

if len(sys.argv) != 2:
    print("Usage: python script.py <cbz_file>")
else:
    process_cbz_file(sys.argv[1])