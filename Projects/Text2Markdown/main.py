# main.py
import sys
from converter.converter import txt_to_md

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py input.txt [output.md]")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    txt_to_md(input_file, output_file)

if __name__ == "__main__":
    main()