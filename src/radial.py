import math

def radial180(landmark_a, landmark_b):    
    # Get the vector from wrist to middle finger tip
    dx = landmark_a[0] - landmark_b[0]  # x difference
    dy = landmark_a[1] - landmark_b[1]  # y difference (note: y increases downward in image coordinates)
    
    # Flip y coordinate since image y-axis is inverted (0 at top, increases downward)
    dy = -dy
    
    # Calculate angle in radians using atan2
    angle_rad = math.atan2(dy, dx)
    
    # Convert to degrees
    angle_deg = math.degrees(angle_rad)
    
    # Normalize to 0-360 range
    if angle_deg < 0:
        angle_deg += 360
    
    # Clamp depending on quadrants
    if angle_deg > 180 and angle_deg <= 270:
        angle_deg = 180
    elif angle_deg > 270:
        angle_deg = 0

    return angle_deg

def radial90(landmark_a, landmark_b):    
    # Get the vector from wrist to middle finger tip
    dx = landmark_a[0] - landmark_b[0]  # x difference
    dy = landmark_a[1] - landmark_b[1]  # y difference (note: y increases downward in image coordinates)
    
    # Flip y coordinate since image y-axis is inverted (0 at top, increases downward)
    dy = -dy
    
    # Calculate angle in radians using atan2
    angle_rad = math.atan2(dy, dx)
    
    # Convert to degrees
    angle_deg = math.degrees(angle_rad)
    
    # Normalize to 0-360 range
    if angle_deg < 0:
        angle_deg += 360
    
    # Clamp depending on quadrants
    if angle_deg > 90 and angle_deg <= 270:
        angle_deg = 90
    elif angle_deg > 270:
        angle_deg = 0
    
    return angle_deg