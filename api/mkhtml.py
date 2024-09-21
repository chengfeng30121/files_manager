from datetime import datetime
import time
import os
import hashlib

def generate_html_template(path: str) -> str:
    table_rows = create_table_rows(path)
    none_files = [(os.path.isfile(os.path.join(path, i))) and i for i in os.listdir(path)]
    if False in none_files:
        none_files.remove(False)
    file_count = str(len(none_files))
    template_path = os.path.join("templates", 'template.html')
    with open(template_path, mode='r', encoding='utf-8') as file:
        template = file.read()
    path = path.replace("\\", "/")
    fake_dir = "/"+"".join([i for i in path.split(os.getcwd())[-1].split("/files/")[1:]])
    print(fake_dir)
    if fake_dir == "/":
        left_dir = ""
    else:
        left_dir = os.path.dirname(fake_dir if not fake_dir.endswith("/") else fake_dir[:-1])
    html_content = template.replace('{path}', fake_dir).replace('{trtablestring}', table_rows).replace('{filenum}', file_count).replace('{left_dir}', left_dir)
    return html_content

def calculate_md5(filepath: str) -> str:
    with open(filepath, mode='rb') as file:
        content = file.read()
    return hashlib.md5(content).hexdigest()

def get_file_modification_time(full_path: str) -> str:
    if os.path.isdir(full_path):
        raise OSError('目录为文件夹！')
    modification_time = str(datetime.fromtimestamp(os.path.getmtime(full_path))).split('.')[0]
    return modification_time

def get_file_size(filepath: str) -> str:
    size = os.path.getsize(filepath)
    
    units = ['B', 'KiB', 'MiB', 'GiB']
    index = 0

    while size >= 1000 and index < len(units) - 1:
        size /= 1024
        index += 1

    return f'{size:.0f} {units[index]}'


def create_table_rows(directory: str) -> str:
    files = os.listdir(directory)
    files.sort()
    rows = ''
    for filename in files:
        full_path = os.path.join(directory, filename)
        link = "".join([i for i in full_path.replace("\\", "/").split(os.getcwd())[-1].split("/files/")[1:]])
        if os.path.isdir(full_path):
            rows += f'''<tr><td><a href="{link}/">{filename}/</a></td><td class="s">-</td><td>-</td><td>-</td></tr>'''
            files.remove(filename)
        else:
            continue
    for filename in files:
        full_path = os.path.join(directory, filename)
        if os.path.isfile(full_path):
            link = "".join([i for i in full_path.replace("\\", "/").split(os.getcwd())[-1].split("/files/")[1:]])
            rows += f'''<tr><td><a href="/download/{link}" download>{filename}</a></td><td class="s">{get_file_size(full_path)}</td><td>{get_file_modification_time(full_path)}</td><td><a href="/{link}/">Preview</a></td></tr>'''
    return rows



if __name__ == '__main__':
    path = os.path.abspath("../..")
    html_result = generate_html_template(path)
    print(html_result, file=open(f'index_{int(time.time())}.html', mode='w', encoding='utf-8'))
