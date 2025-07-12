import pyautogui

def typingHandler(landmarks, last_asl_check, asl_check_threshold): # just a demo poc
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
