# Ephemera <3
# Simple project to learn mediapipe

import cv2 # camera
import mediapipe as mp # hand recognition
import pyautogui # macro
import math
from radial import radial180, radial90
from mouse import m1Handler, m2Handler, cursorHandler, scrollHandler
from asl_typing import typingHandler

# Configuration
pinch_threshold = 0.02

dot_color = (177, 156, 217)
line_color = (255, 255, 255)

mp_max_num_hands = 2
mp_min_detection_confidence = 0.7
mp_min_tracking_confidence = 0.5

cv_frame_width = 640
cv_frame_height = 480
screen_width = 1920
screen_height = 1080

control_mode_array = ["mouse", "asl", "radial"]  # IMPORTANT
last_control_mode_switch_check = 0
control_mode_switch_buffer = 5

# Smoothing factor

cursor_smoothing_factor = 0.5

# Finger coordinate assignments
cursor_landmark = 5
m1_landmark_a = 8
m1_landmark_b = 7
m2_landmark_a = 12
m2_landmark_b = 11
scroll_landmark_a = 4
scroll_landmark_b = 7
scroll_landmark_c = 0
radial_landmark_a = 12
radial_landmark_b = 0
wrist_landmark = 0
normalize_landmark = 9

# ASL
last_asl_check = 0
asl_check_threshold = 5

# Performance optimizations
frames_skipped = 1

def cleanUpCv2ImageToMp(frame):
    frame = cv2.flip(frame, 1)  # Flip for mirror view
    mp_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert to RGB
    return frame, mp_frame

def cleanPAG():
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0  # Remove default pause

def setupCamView(cam):
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, cv_frame_width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cv_frame_height)

def camClose(cam):
    cam.release() # Close the camera
    cv2.destroyAllWindows() # Close all windows

def extractLandmarkPositions(landmarks):
    # Grab positions of all landmarks
    landmarks_positions = []

    for l in landmarks.landmark:
        l_positions = [l.x, l.y]
        landmarks_positions.append(l_positions)

    return landmarks_positions

def normalizeHand(landmark_wrist, landmark_a, landmarks):
    # create a vector from the wrist to landmark a
    dx = landmark_a[0] - landmark_wrist[0]
    dy = landmark_a[1] - landmark_wrist[1]

    # Calculate current angle
    current_angle = math.atan2(dy, dx)

    # target angle is -pi/2 (because things are upside down in coordinate system)
    target_angle = -math.pi / 2

    # Angle to rotate
    da = target_angle - current_angle

    # cos theta and sin theta
    cos_da = math.cos(da)
    sin_da = math.sin(da)

    # Rotate all landmarks around the wrist
    normalized_landmarks = []
    for x, y in landmarks:
        # Let wrist be origin and translate
        tl_x = x - landmark_wrist[0]
        tl_y = y - landmark_wrist[1]

        # Rotate
        rot_x = tl_x * cos_da - tl_y * sin_da
        rot_y = tl_x * sin_da + tl_y * cos_da

        # Translate back
        final_x = rot_x + landmark_wrist[0]
        final_y = rot_y + landmark_wrist[1]

        normalized_landmarks.append([final_x, final_y])

    return normalized_landmarks


def modeSwitchHandler(landmark_a, landmark_b, frame_width, frame_height, mode, rLandmark_a, rLandmark_b):
    if landmark_a[0] < landmark_b[0]:  # Gesture to switch mode
        angle =  radial90(rLandmark_a, rLandmark_b)
        control_count = len(control_mode_array)

        for i in enumerate(control_mode_array):
            index = i[0] + 1
            minAngle = (index - 1) * (90 / control_count) if index > 0 else 0
            maxAngle = (index) * (90 / control_count)

            if angle >= minAngle and angle < maxAngle:
                print(index)
                return index

    return mode

if __name__ == "__main__":
    cleanPAG() # Disable pyautogui failsafe for better performance (these are frame killers lol)
    cam = cv2.VideoCapture(0)  # Open the camera
    setupCamView(cam)

    mp_hands = mp.solutions.hands # Define mediapipe.solutions.hands...
    hands = mp_hands.Hands(
        max_num_hands=mp_max_num_hands, 
        min_detection_confidence=mp_min_detection_confidence,
        static_image_mode=False,
        min_tracking_confidence=mp_min_tracking_confidence
    ) # and instantiate it.

    mp_draw = mp.solutions.drawing_utils # Define drawing utils. For landmark visualization.
    # Customize colors
    dot_style = mp_draw.DrawingSpec(color=dot_color, thickness=2, circle_radius=3)
    line_style = mp_draw.DrawingSpec(color=line_color, thickness=3)

    smoothed_cursor_x, smoothed_cursor_y = None, None

    control_mode = 1

    while True:
        ret, frame = cam.read() # Get return value and a frame from the camera

        if not ret: # If return value is false, exit loop
            break

        frame, mp_frame = cleanUpCv2ImageToMp(frame) # Clean up the frame
        result = hands.process(mp_frame) # run detection on the current frame
        frame_height, frame_width, _ = frame.shape # Get frame details

        if result.multi_hand_landmarks: # check if we have landmarks
            for landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                # handedness is true if right hand
                handedness = True if handedness.classification[0].label == "Right" else False

                # Draw hand landmarks on the frame
                mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS, landmark_drawing_spec=dot_style, connection_drawing_spec=line_style)

                landmarks_positions = extractLandmarkPositions(landmarks) # store positions of landmarks
                landmarks_positions_normalized  = normalizeHand(landmarks_positions[wrist_landmark], landmarks_positions[normalize_landmark], landmarks_positions)

                x = int(landmarks_positions_normalized[8][0] * frame_width)
                y = int(landmarks_positions_normalized[8][1] * frame_height)
                cv2.circle(frame, (x, y), 10, (255, 0, 255), -1)

                if not handedness: # left hand code
                    control_mode = modeSwitchHandler(landmarks_positions[4], landmarks_positions[9], frame_width, frame_height, control_mode, landmarks_positions[radial_landmark_a], landmarks_positions[radial_landmark_b])

                if handedness: # right hand code
                    if control_mode == 1:
                        smoothed_cursor_x, smoothed_cursor_y = cursorHandler(landmarks_positions[cursor_landmark], smoothed_cursor_x, smoothed_cursor_y, cursor_smoothing_factor, screen_width, screen_height, frame_width, frame_height, cv2, frame)
                        m1Handler(landmarks_positions[m1_landmark_a], landmarks_positions[m1_landmark_b], pinch_threshold)
                        m2Handler(landmarks_positions[m2_landmark_a], landmarks_positions[m2_landmark_b], pinch_threshold)
                        scrollHandler(landmarks_positions[scroll_landmark_a], landmarks_positions[scroll_landmark_b], landmarks_positions[scroll_landmark_c])

                    elif control_mode == 2:
                        last_asl_check = typingHandler(landmarks_positions, last_asl_check, asl_check_threshold)

                    elif control_mode == 3:
                        print(radial180(landmarks_positions[radial_landmark_a], landmarks_positions[radial_landmark_b]))

        # Stolen from stackoverflow
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("ruh", frame) # Display that frame in a window

    camClose(cam)