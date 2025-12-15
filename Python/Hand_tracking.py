def track_hand(results):
    left = 0.0
    right = 0.0

    if not results.multi_hand_landmarks:
        return left, right

    for i, hand in enumerate(results.multi_hand_landmarks):
        lm = hand.landmark

        # Gerak tangan dari pergelangan (stabil)
        x = (lm[0].x - 0.5) * 60   # RANGE LIVE2D

        label = results.multi_handedness[i].classification[0].label

        if label == "Left":
            left = x
        else:
            right = x

    return left, right
