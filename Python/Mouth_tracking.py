def track_mouth(lm):
    # Bibir atas & bawah
    open_dist = abs(lm[13].y - lm[14].y)

    # Skala biar kelihatan
    mouth = open_dist * 18

    # Threshold & clamp
    if mouth < 0.15:
        mouth = 0.0

    mouth = min(max(mouth, 0.0), 1.0)

    return mouth
