def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))

def track_eye(lm):
    # Eye Ball
    eyeX = ((lm[33].x + lm[263].x) / 2 - 0.5) * 2
    eyeY = ((lm[159].y + lm[386].y) / 2 - 0.5) * -2

    # EAR (Eye Open)
    left_raw = abs(lm[159].y - lm[145].y)
    right_raw = abs(lm[386].y - lm[374].y)

    # NORMALISASI (INI KUNCI)
    left_open = clamp((left_raw - 0.015) * 40)
    right_open = clamp((right_raw - 0.015) * 40)

    return eyeX, eyeY, left_open, right_open
