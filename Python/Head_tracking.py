def track_head(lm):
    center_x = (lm[234].x + lm[454].x) / 2
    center_y = (lm[10].y + lm[152].y) / 2

    headX = (center_x - 0.5) * 60
    headY = (center_y - 0.5) * -40

    return headX, headY
