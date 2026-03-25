# converter/footnotes.py
import re

def detect_footnote(line: str) -> bool:
    return re.match(r"\[\^\d+\]:", line) is not None