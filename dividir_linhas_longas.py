import sys

def split_long_lines(subtitle_file, max_length=42):
    with open(subtitle_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    splitted_lines = []

    for line in lines:
        # Se não for linha de tempo ou índice
        if "-->" not in line and not line.strip().isdigit() and line.strip() != "":
            # Quebra a linha
            words = line.split()
            temp_line = ""
            for word in words:
                if len(temp_line) + len(word) + 1 <= max_length:
                    temp_line += (word + " ")
                else:
                    splitted_lines.append(temp_line.strip() + "\n")
                    temp_line = word + " "
            splitted_lines.append(temp_line.strip() + "\n")
        else:
            splitted_lines.append(line)

    with open("splitted_" + subtitle_file, 'w', encoding='utf-8') as out:
        out.writelines(splitted_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python split_lines.py <arquivo.srt> [comprimento_máximo_por_linha]")
        sys.exit(1)

    max_len = 42
    if len(sys.argv) == 3:
        max_len = int(sys.argv[2])

    split_long_lines(sys.argv[1], max_len)
