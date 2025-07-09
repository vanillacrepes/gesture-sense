import cv2 # camera
import mediapipe as mp # hand recognition
import pyautogui # macro

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

control_mode_count = 2
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

def calculateDistance(x1, y1, x2, y2): # Place distance code here for cleaner main block
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 # Pythagorean

def m1Handler(landmark_a, landmark_b, frame_width, frame_height):
    if not hasattr(m1Handler, "button_down"):
        m1Handler.button_down = False  # Initialize on first call

    x = int(landmark_a[0] * frame_width)
    y = int(landmark_a[1] * frame_height)

    distance = calculateDistance(landmark_a[0], landmark_a[1], landmark_b[0], landmark_b[1])
    is_lowered = landmark_a[1] > landmark_b[1]

    if (distance < pinch_threshold or is_lowered) and not m1Handler.button_down:
        pyautogui.mouseDown()
        m1Handler.button_down = True
        cv2.putText(frame, "Left Down", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 1)

    elif distance >= pinch_threshold and not is_lowered and m1Handler.button_down:
        pyautogui.mouseUp()
        m1Handler.button_down = False
        cv2.putText(frame, "Left Up", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)

def m2Handler(landmark_a, landmark_b, frame_width, frame_height):
    if not hasattr(m2Handler, "button_down"):
        m2Handler.button_down = False  # Initialize on first call

    x = int(landmark_a[0] * frame_width)
    y = int(landmark_a[1] * frame_height)

    distance = calculateDistance(landmark_a[0], landmark_a[1], landmark_b[0], landmark_b[1])
    is_lowered = landmark_a[1] > landmark_b[1]

    if (distance < pinch_threshold or is_lowered) and not m2Handler.button_down:
        pyautogui.mouseDown(button='right')
        m2Handler.button_down = True
        cv2.putText(frame, "Right Down", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 1)

    elif distance >= pinch_threshold and not is_lowered and m2Handler.button_down:
        pyautogui.mouseUp(button='right')
        m2Handler.button_down = False
        cv2.putText(frame, "Right Up", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)

def cursorHandler(landmark, smoothed_cursor_x, smoothed_cursor_y, frame_width, frame_height):
    x = int(landmark[0] * frame_width)
    y = int(landmark[1] * frame_height)

    # Convert to screen coordinates
    target_cursor_x = int(landmark[0] * screen_width)
    target_cursor_y = int(landmark[1] * screen_height)

    # Initialize smoothed pos on first frame
    if smoothed_cursor_x is None or smoothed_cursor_y is None:
        smoothed_cursor_x, smoothed_cursor_y = target_cursor_x, target_cursor_y

    # Apply exponential smoothing
    smoothed_cursor_x = int(smoothed_cursor_x + (target_cursor_x - smoothed_cursor_x) * cursor_smoothing_factor)
    smoothed_cursor_y = int(smoothed_cursor_y + (target_cursor_y - smoothed_cursor_y) * cursor_smoothing_factor)

    # Move mouse cursor to mapped coordinates
    pyautogui.moveTo(smoothed_cursor_x, smoothed_cursor_y)

    # Draw a circle on the index fingertip
    cv2.circle(frame, (x, y), 10, (255, 0, 255), -1)

    return smoothed_cursor_x, smoothed_cursor_y

def scrollHandler(landmark_a, landmark_b, landmark_c, frame_width, frame_height):
    # Check if landmark a is above to scroll up, and the reverse.
    y1 = landmark_a[1]
    y2 = landmark_b[1]
    y3 = landmark_c[1]

    if y1 > y2 and y1 > y3:
        pyautogui.scroll(-50)
    elif y1 < y2 and y1 < y3:
        pyautogui.scroll(50)

def typingHandler(landmarks, last_asl_check): # just a demo poc
    if last_asl_check > 0:
        last_asl_check += 1
        if last_asl_check < asl_check_threshold:
            return last_asl_check

    # macros
    index_down = landmarks[8][1] > landmarks[6][1]
    middle_down = landmarks[12][1] > landmarks[10][1]
    ring_down = landmarks[16][1] > landmarks[14][1]
    pinky_down = landmarks[20][1] > landmarks[18][1]
    thumb_down = landmarks[4][1] > landmarks[2][1]

    index_up = not index_down
    middle_up = not middle_down
    ring_up = not ring_down
    pinky_up = not pinky_down
    thumb_up = not thumb_down

    index_left = landmarks[8][0] < landmarks[6][0]
    middle_left = landmarks[12][0] < landmarks[10][0]
    ring_left = landmarks[16][0] < landmarks[14][0]
    pinky_left = landmarks[20][0] < landmarks[18][0]
    thumb_left = landmarks[4][0] < landmarks[2][0]

    index_right = not index_left
    middle_right = not middle_left
    ring_right = not ring_left
    pinky_right = not pinky_left
    thumb_right = not thumb_left

    # a
    if index_down and middle_down and ring_down and pinky_down and thumb_up:
        pyautogui.write('a')
        return 1  # Start cooldown

    # b
    elif index_up and middle_up and ring_up and pinky_up and thumb_up and landmarks[4][0] > landmarks[9][0]:
        pyautogui.write('b')
        return 1  # Start cooldown

    # c
    elif index_left and middle_left and ring_left and pinky_left and thumb_left and landmarks[8][1] < landmarks[4][1]:
        pyautogui.write('c')
        return 1  # Start cooldown

    else:
        return last_asl_check

def modeSwitchHandler(landmark_a, landmark_b, frame_width, frame_height, mode, last_check):
    if last_check > 0:
        last_check += 1
        if last_check < control_mode_switch_buffer:
            return mode, last_check

    if landmark_a[0] < landmark_b[0]:  # Gesture to switch mode
        if mode < control_mode_count:
            mode += 1
        else:
            mode = 1
        return mode, 1  # Start cooldown

    return mode, last_check

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

                if not handedness:
                    control_mode, last_control_mode_switch_check = modeSwitchHandler(landmarks_positions[4], landmarks_positions[9], frame_width, frame_height, control_mode, last_control_mode_switch_check)

                if handedness:
                    if control_mode == 1:
                        smoothed_cursor_x, smoothed_cursor_y = cursorHandler(landmarks_positions[cursor_landmark], smoothed_cursor_x, smoothed_cursor_y, frame_width, frame_height)
                        m1Handler(landmarks_positions[m1_landmark_a], landmarks_positions[m1_landmark_b], frame_width, frame_height)
                        m2Handler(landmarks_positions[m2_landmark_a], landmarks_positions[m2_landmark_b], frame_width, frame_height)
                        scrollHandler(landmarks_positions[scroll_landmark_a], landmarks_positions[scroll_landmark_b], landmarks_positions[scroll_landmark_c], frame_width, frame_height)

                    elif control_mode == 2:
                        last_asl_check = typingHandler(landmarks_positions, last_asl_check)

        cv2.imshow("ruh", frame) # Display that frame in a window
        
        # Stolen from stackoverflow
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camClose(cam)