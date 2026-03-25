# converter/table_parser.py
def detect_table(lines, start_index):
    table = []
    i = start_index
    while i < len(lines) and "|" in lines[i]:
        table.append(lines[i])
        i += 1

    if len(table) >= 2:
        header = table[0]
        separator = "|" + "|".join(["---"] * (header.count("|") - 1)) + "|"
        return [header, separator] + table[1:], i

    return None, i