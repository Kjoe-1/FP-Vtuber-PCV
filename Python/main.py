import cv2
import mediapipe as mp

from UDPSender import UDPSender
from Head_tracking import track_head
from Eye_tracking import track_eye
from Mouth_tracking import track_mouth
from Body_tracking import track_body
from Hand_tracking import track_hand

# ===================== MediaPipe Setup =====================
mp_face = mp.solutions.face_mesh
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands

face = mp_face.FaceMesh(
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

hands = mp_hands.Hands(
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# ===================== Camera =====================
cap = cv2.VideoCapture(0)

# ===================== UDP =====================
sender = UDPSender()

# ===================== SMOOTHING (EMA) =====================
smooth = {
    "headX": 0, "headY": 0,
    "eyeX": 0, "eyeY": 0,
    "eyeLOpen": 1, "eyeROpen": 1,
    "mouth": 0,
    "bodyX": 0,
    "handL": 0, "handR": 0
}

def ema(key, value, alpha=0.25):
    smooth[key] = smooth[key] * (1 - alpha) + value * alpha
    return smooth[key]

# ===================== MAIN LOOP =====================
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Mirror camera (BIAR NATURAL)
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_r = face.process(rgb)
    pose_r = pose.process(rgb)
    hand_r = hands.process(rgb)

    # ===================== DEFAULT DATA =====================
    data = {
        "headX": 0, "headY": 0,
        "eyeX": 0, "eyeY": 0,
        "eyeLOpen": 1, "eyeROpen": 1,
        "mouth": 0,
        "bodyX": 0,
        "handL": 0, "handR": 0
    }

    # ===================== FACE =====================
    if face_r.multi_face_landmarks:
        lm = face_r.multi_face_landmarks[0].landmark

        # Head
        headX, headY = track_head(lm)
        data["headX"] = headX
        data["headY"] = headY

        # Eye + Blink
        eyeX, eyeY, eyeL, eyeR = track_eye(lm)
        data["eyeX"] = eyeX
        data["eyeY"] = eyeY
        data["eyeLOpen"] = eyeL
        data["eyeROpen"] = eyeR

        # Mouth
        data["mouth"] = track_mouth(lm)

    # ===================== BODY =====================
    if pose_r.pose_landmarks:
        data["bodyX"] = track_body(pose_r.pose_landmarks.landmark)

    # ===================== HAND =====================
    data["handL"], data["handR"] = track_hand(hand_r)

    hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


    # ===================== SMOOTHING =====================
    for k in smooth:
        data[k] = ema(k, data[k])

    # ===================== SEND TO UNITY =====================
    sender.send(data)

    # ===================== DEBUG WINDOW =====================
    cv2.imshow("Live Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

# ===================== CLEANUP =====================
cap.release()
cv2.destroyAllWindows()
