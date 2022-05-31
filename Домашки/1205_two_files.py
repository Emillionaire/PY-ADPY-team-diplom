import os
import glob

BASE_PATH = os.getcwd()
# FILES_DIR_NAME = 'sorted'
# full_path = os.path.join(BASE_PATH, FILES_DIR_NAME)
# result_file = 'result.txt'
files_dir = {}
sorted_files_dir = {}

def take_lines(FILES_DIR_NAME, result_file):
    full_path = os.path.join(BASE_PATH, FILES_DIR_NAME)
    for filename in glob.glob(os.path.join(full_path, '*.txt')):
        if result_file not in filename:
            with open(filename, encoding='utf-8') as f:
                files_dir[os.path.basename(f.name)] = len(f.readlines())
                sorted_tuples = sorted(files_dir.items(), key=lambda item: item[1])
                sorted_files_dir = {k: v for k, v in sorted_tuples}
    return(sorted_files_dir)

def write_new_file(FILES_DIR_NAME, result_file):
    a = take_lines(FILES_DIR_NAME, result_file)
    full_path = os.path.join(BASE_PATH, FILES_DIR_NAME)
    with open(os.path.join(full_path, result_file), 'w', encoding='utf-8',) as res:
        for key in a.keys():
            sorted_file_name = os.path.join(full_path, key)
            with open(sorted_file_name, encoding='utf-8') as f:
                res.write(f'{os.path.basename(f.name)}\n{a[key]}\n')
                for line in f:
                    res.write(line)
                res.write(f'\n')


write_new_file('sorted', 'rec.txt')
print(take_lines('sorted', 'rec.txt'))
