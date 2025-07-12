import pyautogui # macro

def calculateDistance(x1, y1, x2, y2): # Place distance code here for cleaner main block
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 # Pythagorean

def m1Handler(landmark_a, landmark_b, pinch_threshold):
    if not hasattr(m1Handler, "button_down"):
        m1Handler.button_down = False  # Initialize on first call

    distance = calculateDistance(landmark_a[0], landmark_a[1], landmark_b[0], landmark_b[1])
    is_lowered = landmark_a[1] > landmark_b[1]

    if (distance < pinch_threshold or is_lowered) and not m1Handler.button_down:
        pyautogui.mouseDown()
        m1Handler.button_down = True

    elif distance >= pinch_threshold and not is_lowered and m1Handler.button_down:
        pyautogui.mouseUp()
        m1Handler.button_down = False

def m2Handler(landmark_a, landmark_b, pinch_threshold):
    if not hasattr(m2Handler, "button_down"):
        m2Handler.button_down = False  # Initialize on first call

    distance = calculateDistance(landmark_a[0], landmark_a[1], landmark_b[0], landmark_b[1])
    is_lowered = landmark_a[1] > landmark_b[1]

    if (distance < pinch_threshold or is_lowered) and not m2Handler.button_down:
        pyautogui.mouseDown(button='right')
        m2Handler.button_down = True

    elif distance >= pinch_threshold and not is_lowered and m2Handler.button_down:
        pyautogui.mouseUp(button='right')
        m2Handler.button_down = False

def cursorHandler(landmark, smoothed_cursor_x, smoothed_cursor_y, cursor_smoothing_factor, screen_width, screen_height, frame_width, frame_height, cv2, frame):
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

def scrollHandler(landmark_a, landmark_b, landmark_c):
    # Check if landmark a is above to scroll up, and the reverse.
    y1 = landmark_a[1]
    y2 = landmark_b[1]
    y3 = landmark_c[1]

    if y1 > y2 and y1 > y3:
        pyautogui.scroll(-50)
    elif y1 < y2 and y1 < y3:
        pyautogui.scroll(50)