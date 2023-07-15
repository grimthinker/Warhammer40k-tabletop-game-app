from geometry import Line
from dc import Position


def make_line(color: tuple[int, int, int], position: tuple[int, int]) -> Line:
    line = Line(color=color, position=position, end=position)
    return line

