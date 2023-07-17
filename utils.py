import math
from typing import TYPE_CHECKING

from dc import Position, Offset


if TYPE_CHECKING:
    from geometry import Line


def length(a_pos, b_pos):
    start_x, start_y = a_pos
    end_x, end_y = b_pos
    offset = Offset(end_x - start_x, end_y - start_y)
    return offset.distance


def distance_w(a_pos, b_pos, c_pos):
    """
    Returns the distance between line(a_pos, b_pos) and point(c_pos)
    :param a_pos:
    :param b_pos:
    :param c_pos:
    :return:
    """
    ax, ay = a_pos
    bx, by = b_pos
    x, y = c_pos
    value = ((x - ax) * (bx - ax) + (y - ay) * (by - ay)) / ((bx - ax)**2 + (by - ay)**2)
    if value < 0:
        value = 0
    elif value > 1:
        value = 1
    return math.hypot(ax - x + (bx - ax) * value, ay - y + (by - ay) * value)


def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]

def ang(A: 'Line', B: 'Line'):
    vA = A.vector
    vB = B.vector
    dot_prod = dot(vA, vB)
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5
    cos_ = dot_prod / magA / magB
    angle = math.acos(cos_)
    ang_deg = math.degrees(angle) % 360
    if ang_deg - 90 >= 0:
        return 180 - ang_deg
    else:
        return ang_deg


def find_correction(over, A: 'Line', B: 'Line'):
    dragging_angle = ang(A, B)
    return over * math.cos(dragging_angle) * 1.1

