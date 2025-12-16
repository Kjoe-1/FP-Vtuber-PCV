def track_hand(results):
    armL = 0
    armR = 0

    if not results.multi_hand_landmarks:
        return armL, armR

    for i, hand in enumerate(results.multi_hand_landmarks):
        lm = hand.landmark
        label = results.multi_handedness[i].classification[0].label

        wrist_y = lm[0].y

        # gesture sederhana & stabil
        if wrist_y < 0.35:
            v = 25    # angkat
        elif wrist_y < 0.45:
            v = 15    # setengah
        else:
            v = 0     # turun

        if label == "Left":
            armL = v
        else:
            armR = v

    return armL, armR
