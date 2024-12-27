import re
import sys

def fix_overlaps(subtitle_file):
    timecode_pattern = re.compile(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})')
    
    def time_to_ms(hours, minutes, seconds, millis):
        return (int(hours)*3600 + int(minutes)*60 + int(seconds))*1000 + int(millis)
    
    def ms_to_time(ms):
        h = ms // 3600000
        ms %= 3600000
        m = ms // 60000
        ms %= 60000
        s = ms // 1000
        ms %= 1000
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    with open(subtitle_file, 'r', encoding='utf-8') as f:
        blocks = f.read().strip().split('\n\n')

    for i in range(len(blocks) - 1):
        lines_current = blocks[i].split('\n')
        lines_next = blocks[i+1].split('\n')
        
        # A linha de tempo é geralmente a segunda linha de cada bloco
        # Exemplo: "00:00:12,500 --> 00:00:15,000"
        if len(lines_current) < 2 or len(lines_next) < 2:
            continue

        current_time_line = lines_current[1]
        next_time_line = lines_next[1]

        start_current, end_current = current_time_line.split('-->')
        start_next, end_next = next_time_line.split('-->')

        start_current = start_current.strip()
        end_current = end_current.strip()
        start_next = start_next.strip()
        end_next = end_next.strip()

        # Converte para milissegundos
        hc1, mc1, sc1, msc1 = timecode_pattern.search(start_current).groups()
        hc2, mc2, sc2, msc2 = timecode_pattern.search(end_current).groups()

        hn1, mn1, sn1, msn1 = timecode_pattern.search(start_next).groups()
        hn2, mn2, sn2, msn2 = timecode_pattern.search(end_next).groups()

        start_ms_current = time_to_ms(hc1, mc1, sc1, msc1)
        end_ms_current   = time_to_ms(hc2, mc2, sc2, msc2)
        start_ms_next    = time_to_ms(hn1, mn1, sn1, msn1)
        end_ms_next      = time_to_ms(hn2, mn2, sn2, msn2)

        # Se o próximo inicia antes do fim do atual, ajustar
        if start_ms_next < end_ms_current:
            start_ms_next = end_ms_current + 50  # adiciona 50 ms de intervalo

            # Atualiza a linha de tempo do bloco "next"
            new_start_str = ms_to_time(start_ms_next)
            new_end_str   = ms_to_time(end_ms_next if end_ms_next > start_ms_next else start_ms_next + 1000)
            lines_next[1] = f"{new_start_str} --> {new_end_str}"
            blocks[i+1] = '\n'.join(lines_next)

    # Grava de volta o arquivo
    with open("fixed_" + subtitle_file, 'w', encoding='utf-8') as out:
        out.write('\n\n'.join(blocks))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python fix_overlaps.py <arquivo.srt>")
        sys.exit(1)

    fix_overlaps(sys.argv[1])
