import os
import json

def read_io(filename: str, range: str = None) -> bytes:
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"File {filename} not found or not a file.")
    
    size = os.path.getsize(filename)
    
    if range is None:
        if size > 1024 * 1024 * 20:
            raise ValueError("File too large for direct read.")
        
        with open(filename, "rb") as f:
            return f.read()
    
    start, end = range.split("-")
    start = int(start) if start else 0
    end = int(end) if end else size - 1
    
    if start > end or end > size:
        raise ValueError("Invalid range.")
    
    with open(filename, "rb") as f:
        f.seek(start)
        return f.read(end - start + 1)

def get_real_filename(filename: str) -> str:
    if filename.endswith("/"):
        if os.path.exists(os.path.join(os.getcwd(), "files", filename[:-1])):
            return os.path.join(os.getcwd(), "files", filename[:-1])
    return os.path.join(os.getcwd(), "files", filename)

def read_content_type(filename: str) -> str:
    extension = os.path.splitext(filename)[1]
    content_type_mapping = json.loads(open(os.path.join(os.getcwd(), "templates", "content-type.json")).read())
    return content_type_mapping.get(extension, "application/octet-stream")