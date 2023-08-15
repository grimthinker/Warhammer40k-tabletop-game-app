import math
from typing import TYPE_CHECKING
import numpy

from basic_data.dc import Offset


if TYPE_CHECKING:
    from geometry import Line


def to_real_scale(pos, scale, offset_x, offset_y, angle):
    x, y = pos
    cx, cy = (x + offset_x) / scale, (y + offset_y) / scale
    pos = numpy.array([cx, cy])
    x, y = numpy.dot(pos, rot_matrix(-angle))
    return x, y

def to_screen_scale(pos, scale, offset_x, offset_y, angle):
    pos = numpy.array(pos)
    x, y = numpy.dot(pos, rot_matrix(angle))
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
    value = ((x - ax) * (bx - ax) + (y - ay) * (by - ay)) / ((bx - ax)**2 + (by - ay)**2 + 0.0000001)
    if value < 0:
        value = 0
    elif value > 1:
        value = 1
    return math.hypot(ax - x + (bx - ax) * value, ay - y + (by - ay) * value)


def ccw(A, B, C):
    ax, ay = A
    bx, by = B
    cx, cy = C
    return (cy - ay) * (bx - ax) > (by - ay) * (cx - ax)


def segments_intersect(segmentA, segmentB):
    return ccw(segmentA.position, segmentB.position, segmentB.end) != \
           ccw(segmentA.end, segmentB.position, segmentB.end) and \
           ccw(segmentA.position, segmentA.end, segmentB.position) != \
           ccw(segmentA.position, segmentA.end, segmentB.end)


def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]

def ang(vA: tuple[float, float], vB: tuple[float, float], full=False):
    dot_prod = dot(vA, vB)
    magA = dot(vA, vA)**0.5 + 0.00001
    magB = dot(vB, vB)**0.5 + 0.00001
    cos_ = dot_prod / magA / magB
    angle = math.acos(cos_)
    ang_deg = math.degrees(angle) % 360
    if ang_deg - 180 >= 0:
        return math.pi - angle
    else:
        return angle


def ang_alt(vA: tuple[float, float]):
    ret = math.atan2(*vA) + math.pi / 2
    return ret


def slope(v: tuple[float, float]):
    x, y = v
    return y/x

def find_angle(A: 'Line', B: 'Line'):
    vA = A.vector
    vB = B.vector
    angle = ang(vA, vB)
    return angle


def check_intersection(A: 'Line', B: 'Line'):
    ax1, ay1 = A.position
    ax2, ay2 = A.end
    bx1, by1 = B.position
    bx2, by2 = B.end
    v1 = (bx2-bx1) * (ay1-by1) - (by2-by1) * (ax1-bx1)
    v2 = (bx2-bx1) * (ay2-by1) - (by2-by1) * (ax2-bx1)
    v3 = (ax2-ax1) * (by1-ay1) - (ay2-ay1) * (bx1-ax1)
    v4 = (ax2-ax1) * (by2-ay1) - (ay2-ay1) * (bx2-ax1)
    return v1 * v2 < 0 and v3 * v4 < 0


def find_correction_circle(error: float, radiusA: float, radiusB: float):
    correction = error * 0.2 * ((radiusA + radiusB) / radiusB)
    return correction

def rot_matrix(theta):
    return numpy.array([[numpy.cos(theta), -numpy.sin(theta)],
                                   [numpy.sin(theta), numpy.cos(theta)]])

