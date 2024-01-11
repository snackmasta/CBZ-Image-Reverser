import os
import sys
import uuid
import zipfile
import tempfile
import shutil

from PIL import Image

def reverse_file_order(directory):
    files = os.listdir(directory)
    i = 0
    while i < len(files) - 1:
        file1 = os.path.join(directory, files[i])
        image1 = Image.open(file1)
        if image1.size[0] > image1.size[1]:  # Skip landscape pages
            i += 1
            continue
        j = i + 1
        while j < len(files):
            file2 = os.path.join(directory, files[j])
            image2 = Image.open(file2)
            if image2.size[0] > image2.size[1]:  # Skip landscape pages
                j += 1
                continue
            temp = os.path.join(directory, str(uuid.uuid4()))
            try:
                os.rename(file1, temp)
                os.rename(file2, file1)
                os.rename(temp, file2)
            except Exception as e:
                print(f"Error swapping files {files[i]} and {files[j]}: {e}")
            break
        i = j + 1

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