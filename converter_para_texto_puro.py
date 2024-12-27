import re
import sys

def srt_to_text(subtitle_file):
    with open(subtitle_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    text_content = []
    timecode_pattern = re.compile(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}')

    for line in lines:
        # Ignora linhas que sejam só número do bloco ou tempo de legenda
        if line.strip().isdigit() or timecode_pattern.search(line):
            continue
        # Ignora linhas em branco
        if line.strip() == "":
            continue
        text_content.append(line)

    with open("output.txt", 'w', encoding='utf-8') as out:
        out.writelines(text_content)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python srt_to_text.py <arquivo.srt>")
        sys.exit(1)

    srt_to_text(sys.argv[1])
