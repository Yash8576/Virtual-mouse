import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import os

os.environ['GLOG_minloglevel'] = '2'

cap = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
draw = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()

# Cooldowns
last_left_click_time = 0
last_right_click_time = 0
last_zoom_time = 0
last_scroll_time = 0

# Movement tracking
prev_avg_y = None
prev_avg_x = None
scroll_prev_y = None
scroll_prev_x = None

def get_finger_states(lm):
    tips = [4, 8, 12, 16, 20]
    pip = [2, 6, 10, 14, 18]
    return [lm[t].y < lm[p].y for t, p in zip(tips, pip)]

def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

while True:
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        lm = hand.landmark
        draw.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)

        fingers = get_finger_states(lm)

        # Finger tips
        thumb_tip = int(lm[4].x * w), int(lm[4].y * h)
        idx_tip = int(lm[8].x * w), int(lm[8].y * h)
        mid_tip = int(lm[12].x * w), int(lm[12].y * h)
        ring_tip = int(lm[16].x * w), int(lm[16].y * h)
        pinky_tip = int(lm[20].x * w), int(lm[20].y * h)

        # Move mouse using THUMB instead of index
        screen_x = np.interp(lm[4].x, [0, 1], [0, screen_w])
        screen_y = np.interp(lm[4].y, [0, 1], [0, screen_h])
        pyautogui.moveTo(screen_x, screen_y)

        current_time = time.time()

        # Distance threshold for clicks (adjust for comfort)
        CLICK_THRESHOLD = 60

        # Right Click (thumb + index + middle within threshold)
        if (
            distance(idx_tip, mid_tip) < CLICK_THRESHOLD and
            distance(idx_tip, thumb_tip) < CLICK_THRESHOLD and
            distance(mid_tip, thumb_tip) < CLICK_THRESHOLD and
            current_time - last_right_click_time > 0.7
        ):
            pyautogui.rightClick()
            last_right_click_time = current_time

        # Left Click (thumb + index within threshold)
        elif (
            distance(idx_tip, thumb_tip) < CLICK_THRESHOLD and
            current_time - last_left_click_time > 0.5
        ):
            pyautogui.click()
            last_left_click_time = current_time

        # Zoom (3 fingers: index, middle, ring)
        if fingers[1] and fingers[2] and fingers[3] and not fingers[4]:
            avg_y = (lm[8].y + lm[12].y + lm[16].y) / 3
            avg_x = (lm[8].x + lm[12].x + lm[16].x) / 3

            if prev_avg_y is not None and prev_avg_x is not None:
                dy = prev_avg_y - avg_y
                dx = avg_x - prev_avg_x

                vertical_thresh = 0.06
                horizontal_thresh = 0.05

                if dy > vertical_thresh and dy > abs(dx) and current_time - last_zoom_time > 1:
                    pyautogui.hotkey('command', '+')
                    last_zoom_time = current_time
                elif dx > horizontal_thresh and dx > abs(dy) and current_time - last_zoom_time > 1:
                    pyautogui.hotkey('command', '-')
                    last_zoom_time = current_time

            prev_avg_y = avg_y
            prev_avg_x = avg_x
        else:
            prev_avg_y = None
            prev_avg_x = None

        # Scroll (4 fingers: index, middle, ring, pinky)
        if fingers[1] and fingers[2] and fingers[3] and fingers[4]:
            scroll_y = (lm[8].y + lm[12].y + lm[16].y + lm[20].y) / 4
            scroll_x = (lm[8].x + lm[12].x + lm[16].x + lm[20].x) / 4

            if scroll_prev_y is not None and scroll_prev_x is not None:
                dy = scroll_prev_y - scroll_y
                dx = scroll_x - scroll_prev_x

                vertical_thresh = 0.06
                horizontal_thresh = 0.05

                if dy > vertical_thresh and dy > abs(dx) and current_time - last_scroll_time > 0.3:
                    pyautogui.scroll(-40)  # scroll down
                    last_scroll_time = current_time
                elif dx > horizontal_thresh and dx > abs(dy) and current_time - last_scroll_time > 0.3:
                    pyautogui.scroll(40)   # scroll up
                    last_scroll_time = current_time

            scroll_prev_y = scroll_y
            scroll_prev_x = scroll_x
        else:
            scroll_prev_y = None
            scroll_prev_x = None

    cv2.imshow("Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()