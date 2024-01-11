import os

def swap_file_names(directory):
    files = os.listdir(directory)
    for i in range(0, len(files), 2):
        if (i+1) < len(files):
            file1 = os.path.join(directory, files[i])
            file2 = os.path.join(directory, files[i+1])
            temp = os.path.join(directory, 'temp')
            try:
                os.rename(file1, temp)
                os.rename(file2, file1)
                os.rename(temp, file2)
            except Exception as e:
                print(f"Error swapping files {files[i]} and {files[i+1]}: {e}")
    if len(files) % 2 != 0:
        file1 = os.path.join(directory, files[0])
        file2 = os.path.join(directory, files[-1])
        temp = os.path.join(directory, 'temp')
        try:
            os.rename(file1, temp)
            os.rename(file2, file1)
            os.rename(temp, file2)
        except Exception as e:
            print(f"Error swapping files {files[0]} and {files[-1]}: {e}")

swap_file_names(r"E:\Python\tes")