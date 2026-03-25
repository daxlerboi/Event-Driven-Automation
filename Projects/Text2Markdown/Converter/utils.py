# converter/utils.py
from pathlib import Path

def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(file_path: str, content: str):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def file_exists(file_path: str) -> bool:
    return Path(file_path).exists()