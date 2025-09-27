import math
from settings import width, height

def get_angle(mouse_x, mouse_y):
    origin_x, origin_y = width//2, height//2
    target_x, target_y = mouse_x, mouse_y
    dx = target_x - origin_x
    dy = target_y - origin_y
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return angle_deg

def angle_to_cords(x, y, distance=10, angle=45):
    x = 0
    y = 0
    angle_degrees = angle
    angle_radians = math.radians(angle_degrees)
    dy = distance * math.cos(angle_radians)
    dx = distance / math.sin(angle_radians)
    x += dx
    y += dy
    return int(x), int(y)

