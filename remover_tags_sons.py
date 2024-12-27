import re
import sys

def remove_sound_descriptions(subtitle_file):
    with open(subtitle_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    pattern = re.compile(r'[\(\[].*?[\)\]]')  # remove tudo entre ( ) ou [ ]

    for line in lines:
        # Remove padrões de ruídos ou nomes entre parênteses/colchetes
        new_line = re.sub(pattern, '', line)
        cleaned_lines.append(new_line)

    with open("cleaned_" + subtitle_file, 'w', encoding='utf-8') as out:
        out.writelines(cleaned_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python remove_sounds.py <arquivo.srt>")
        sys.exit(1)

    remove_sound_descriptions(sys.argv[1])
