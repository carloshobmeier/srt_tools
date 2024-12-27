# pip install googletrans==4.0.0-rc1
from googletrans import Translator

def translate_srt(subtitle_file, src_lang='en', dest_lang='pt'):
    translator = Translator()
    with open(subtitle_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    translated_lines = []
    buffer_text = []

    for line in lines:
        # Se for linha de tempo ou índice, não traduz
        if line.strip().isdigit() or "-->" in line or line.strip() == "":
            # Se havia texto acumulado no buffer, traduz
            if buffer_text:
                joined_text = ' '.join(buffer_text)
                try:
                    translation = translator.translate(joined_text, src=src_lang, dest=dest_lang)
                    translated_lines.append(translation.text + "\n")
                except Exception as e:
                    translated_lines.append(joined_text + "\n")
                buffer_text = []
            translated_lines.append(line)
        else:
            # Acumula texto para traduzir
            buffer_text.append(line.strip())

    # Traduz o que sobrou no buffer
    if buffer_text:
        joined_text = ' '.join(buffer_text)
        try:
            translation = translator.translate(joined_text, src=src_lang, dest=dest_lang)
            translated_lines.append(translation.text + "\n")
        except Exception as e:
            translated_lines.append(joined_text + "\n")

    with open("translated_" + subtitle_file, 'w', encoding='utf-8') as out:
        out.writelines(translated_lines)
