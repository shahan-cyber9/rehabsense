"""Joint-angle geometry helpers."""

import math


def calculate_angle(a, b, c):
    """Calculate the angle at point b given three points a, b, c."""
    ax, ay = a
    bx, by = b
    cx, cy = c

    v1 = (ax - bx, ay - by)
    v2 = (cx - bx, cy - by)

    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    mag1 = math.hypot(*v1)
    mag2 = math.hypot(*v2)

    if mag1 == 0 or mag2 == 0:
        return None

    cos_theta = dot_product / (mag1 * mag2)
    cos_theta = max(-1.0, min(1.0, cos_theta))
    
    return math.degrees(math.acos(cos_theta))