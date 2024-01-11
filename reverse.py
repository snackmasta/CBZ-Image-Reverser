import os
import sys
import uuid

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

if len(sys.argv) != 2:
    print("Usage: python script.py <directory>")
else:
    reverse_file_order(sys.argv[1])