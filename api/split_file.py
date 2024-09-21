import os
import json
def split_file(file_path, chunk_size=20 * 1024 * 1024, output_dir='chunks'):
    """ 
    将文件按指定大小切分成多个小文件，并返回包含所有分块信息的字典。
    :param file_path: 原始文件路径 param chunk_size: 
    :每个分块的最大大小，默认为20MB param output_dir: 
    :分块文件存放目录，默认为'chunks' return: 包含分块信息的字典
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    # 获取文件名和扩展名
    base_name = os.path.basename(file_path) name, ext = 
    os.path.splitext(base_name)
    # 读取文件并切分
    with open(file_path, 'rb') as f: chunk_count = 0 files_info = [] 
        while True:
            chunk_data = f.read(chunk_size) if not chunk_data: break 
            chunk_filename = 
            f"{output_dir}/{name}_part_{chunk_count}{ext}" with 
            open(chunk_filename, 'wb') as chunk_file:
                chunk_file.write(chunk_data) 
            files_info.append({"name": 
            os.path.basename(chunk_filename), "size": 
            len(chunk_data)}) chunk_count += 1
    # 创建文件清单
    file_list = { "name": name, "files": files_info, "size": 
        os.path.getsize(file_path)
    }
    # 写入JSON文件
    with open(f"{output_dir}/file_list.json", 'w', encoding='utf-8') 
    as json_file:
        json.dump(file_list, json_file, ensure_ascii=False, indent=4) 
    return file_list
# 使用示例
file_path = 'path/to/your/large_file.txt' # 替换为你的文件路径
split_file(file_path)
