import re
import sys

def clean_subtitle_format(subtitle_file):
    with open(subtitle_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned = []
    html_tag_pattern = re.compile(r'<.*?>')  # remove tags como <b>, <i>, etc.

    for line in lines:
        line = re.sub(html_tag_pattern, '', line)
        cleaned.append(line)

    with open("formatted_" + subtitle_file, 'w', encoding='utf-8') as out:
        out.writelines(cleaned)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python clean_format.py <arquivo.srt>")
        sys.exit(1)

    clean_subtitle_format(sys.argv[1])
