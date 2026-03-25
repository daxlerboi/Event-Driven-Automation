# converter/code_parser.py
def detect_code_block(line: str) -> bool:
    langs = ["python", "bash", "javascript", "html", "css", "json", "text"]
    return line.strip().lower() in langs