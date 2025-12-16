def track_mouth(lm):
    open_dist = abs(lm[13].y - lm[14].y)
    mouth = open_dist * 30

    if mouth < 0.2:
        mouth = 0.0

    return min(mouth, 1.0)
