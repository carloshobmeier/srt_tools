import sys

def shift_subtitle_time(subtitle_file, shift_seconds):
    with open(subtitle_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    def shift_timecode(timecode, shift_s):
        # Formato padrão: HH:MM:SS,mmm
        h, m, s_milli = timecode.split(':')
        s, milli = s_milli.split(',')
        total_millis = (int(h) * 3600 + int(m) * 60 + int(s)) * 1000 + int(milli)
        total_millis += int(shift_s * 1000)

        if total_millis < 0:
            total_millis = 0  # garante que não fique negativo

        new_h = total_millis // 3600000
        remainder = total_millis % 3600000
        new_m = remainder // 60000
        remainder = remainder % 60000
        new_s = remainder // 1000
        new_milli = remainder % 1000

        return f"{new_h:02d}:{new_m:02d}:{new_s:02d},{new_milli:03d}"

    with open("shifted_" + subtitle_file, 'w', encoding='utf-8') as out:
        for line in lines:
            if "-->" in line:
                start, arrow, end = line.split()
                new_start = shift_timecode(start, shift_seconds)
                new_end = shift_timecode(end, shift_seconds)
                out.write(f"{new_start} --> {new_end}\n")
            else:
                out.write(line)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python shift_subtitle.py <arquivo.srt> <segundos de atraso (pode ser negativo)>")
        sys.exit(1)

    subtitle_path = sys.argv[1]
    shift_s = float(sys.argv[2])
    shift_subtitle_time(subtitle_path, shift_s)
