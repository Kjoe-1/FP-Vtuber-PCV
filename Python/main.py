import cv2
import mediapipe as mp
import time

from UDPSender import UDPSender
from Head_tracking import track_head
from Eye_tracking import track_eye
from Mouth_tracking import track_mouth
from Hand_tracking import track_hand

# ===================== MediaPipe Setup (RINGAN) =====================
mp_face = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

face = mp_face.FaceMesh(
    refine_landmarks=True,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
)

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# ===================== Camera (LOW LOAD) =====================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
cap.set(cv2.CAP_PROP_FPS, 30)

# ===================== UDP =====================
sender = UDPSender()

# ===================== SMOOTHING STORAGE =====================
smooth = {
    "headX": 0, "headY": 0,
    "eyeX": 0, "eyeY": 0,
    "eyeLOpen": 1, "eyeROpen": 1,
    "mouth": 0,
    "armL": 0, "armR": 0,
    "bodyX": 0, "bodyY": 0, "bodyZ": 0
}

def ema(key, value, alpha):
    smooth[key] = smooth[key] * (1 - alpha) + value * alpha
    return smooth[key]

# ===================== MAIN LOOP =====================
while True:
    ret, frame = cap.read()
    if not ret:
        time.sleep(0.03)
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_r = face.process(rgb)
    hand_r = hands.process(rgb)

    # ===================== DEFAULT DATA =====================
    data = {
        "headX": 0, "headY": 0,
        "eyeX": 0, "eyeY": 0,
        "eyeLOpen": 1, "eyeROpen": 1,
        "mouth": 0,
        "armL": 0, "armR": 0,
        "bodyX": 0, "bodyY": 0, "bodyZ": 0
    }

    # ===================== FACE =====================
    if face_r.multi_face_landmarks:
        lm = face_r.multi_face_landmarks[0].landmark

        hx, hy = track_head(lm)
        ex, ey, el, er = track_eye(lm)

        data["headX"] = hx
        data["headY"] = hy

        data["eyeX"] = ex
        data["eyeY"] = ey
        data["eyeLOpen"] = el
        data["eyeROpen"] = er

        data["mouth"] = track_mouth(lm)

        # ===================== BODY FOLLOW HEAD (REAL-TIME) =====================
        data["bodyX"] = hx * 0.35
        data["bodyY"] = hy * 0.25
        data["bodyZ"] = hx * 0.2

    # ===================== HAND (GESTURE-BASED) =====================
    data["handL"], data["handR"] = track_hand(hand_r)

    # ===================== SAFE SMOOTHING =====================
    data["headX"] = ema("headX", data["headX"], 0.45)
    data["headY"] = ema("headY", data["headY"], 0.45)

    data["eyeX"] = ema("eyeX", data["eyeX"], 0.7)
    data["eyeY"] = ema("eyeY", data["eyeY"], 0.7)

    data["eyeLOpen"] = ema("eyeLOpen", data["eyeLOpen"], 0.8)
    data["eyeROpen"] = ema("eyeROpen", data["eyeROpen"], 0.8)

    data["mouth"] = ema("mouth", data["mouth"], 0.8)
    
    data["armL"], data["armR"] = track_hand(hand_r)

    data["armL"] = ema("armL", data["armL"], 0.5)
    data["armR"] = ema("armR", data["armR"], 0.5)

    data["bodyX"] = ema("bodyX", data["bodyX"], 0.4)
    data["bodyY"] = ema("bodyY", data["bodyY"], 0.4)
    data["bodyZ"] = ema("bodyZ", data["bodyZ"], 0.4)

    # ===================== SEND =====================
    sender.send(data)

    # ===================== DISPLAY =====================
    cv2.imshow("Tracking (Safe Mode)", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

    # ===================== CPU LIMITER =====================
    time.sleep(0.02)

# ===================== CLEANUP =====================
cap.release()
cv2.destroyAllWindows()
