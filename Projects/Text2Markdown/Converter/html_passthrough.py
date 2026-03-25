# converter/html_passthrough.py
def is_html(line: str) -> bool:
    return line.strip().startswith("<") and line.strip().endswith(">")