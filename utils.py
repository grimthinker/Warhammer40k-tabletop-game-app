import math
from typing import TYPE_CHECKING

from dc import Position, Offset


if TYPE_CHECKING:
    from geometry import Line, Circle


def to_real_scale(pos, scale, offset_x, offset_y):
    x, y = pos
    return (x + offset_x) / scale, (y + offset_y) / scale

def to_screen_scale(pos, scale, offset_x, offset_y):
    x, y = pos
    return scale * x - offset_x, scale * y - offset_y

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

def ang(vA: tuple[float, float], vB: tuple[float, float]):
    dot_prod = dot(vA, vB)
    magA = dot(vA, vA)**0.5 + 0.00001
    magB = dot(vB, vB)**0.5 + 0.00001
    cos_ = dot_prod / magA / magB
    angle = math.acos(cos_)
    ang_deg = math.degrees(angle) % 180
    if ang_deg - 90 >= 0:
        return math.pi/2 - angle
    else:
        return angle


def find_correction(error: float, A: 'Line', B: 'Line'):
    vA = A.vector
    vB = B.vector
    angle = ang(vA, vB)
    correction = error * (math.cos(angle) + error * 0.01) * 1.002
    return correction


def find_correction_circle(error: float, radiusA: float, radiusB: float):
    correction = error * 0.2 * ((radiusA + radiusB) / radiusB)
    return correction

