# converter/converter.py
from .utils import read_file, write_file, file_exists
from .formatters import format_inline
from .table_parser import detect_table
from .code_parser import detect_code_block
from .math_parser import detect_math_block
from .footnotes import detect_footnote
from .html_passthrough import is_html

def convert_to_markdown(text: str) -> str:
    lines = text.splitlines()
    md_lines = []
    in_code_block = False
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        # Code blocks
        if detect_code_block(stripped):
            md_lines.append(f"```{stripped.lower()}")
            in_code_block = True
            i += 1
            continue

        if in_code_block:
            if stripped == "":
                md_lines.append("```")
                in_code_block = False
            else:
                md_lines.append(line)
            i += 1
            continue

        # Tables
        table, new_i = detect_table(lines, i)
        if table:
            md_lines.extend(table)
            i = new_i
            continue

        # Horizontal rules
        if stripped in ["---", "***"]:
            md_lines.append("---")
        # Headings
        elif stripped.isupper() and len(stripped) < 60:
            md_lines.append(f"# {stripped.title()}")
        elif stripped.endswith(":") and len(stripped) < 60:
            md_lines.append(f"## {stripped[:-1]}")
        # Blockquote
        elif stripped.startswith(">"):
            md_lines.append(stripped)
        # Task list
        elif stripped.lower().startswith("- ["):
            md_lines.append(stripped)
        # Bullet / numbered
        elif stripped.startswith(("-", "*", "+")) or stripped[0].isdigit():
            md_lines.append(stripped)
        # Footnotes
        elif detect_footnote(stripped):
            md_lines.append(stripped)
        # Math
        elif detect_math_block(stripped):
            md_lines.append("$$")
        # HTML passthrough
        elif is_html(stripped):
            md_lines.append(line)
        # Empty line
        elif stripped == "":
            md_lines.append("")
        # Normal text → inline formatting
        else:
            md_lines.append(format_inline(line))

        i += 1

    return "\n".join(md_lines)


def txt_to_md(input_file: str, output_file: str = None):
    if not file_exists(input_file):
        print("❌ File not found!")
        return

    text = read_file(input_file)

    markdown = convert_to_markdown(text)

    if not output_file:
        from pathlib import Path
        output_file = Path(input_file).with_suffix(".md")

    write_file(output_file, markdown)
    print(f"✅ Converted successfully: {output_file}")