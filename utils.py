from typing import Generator, Callable
from multipledispatch import dispatch

from constants import *

def sign(num: int | float) -> int:
    """Returns the sign of the num (+/-) as -1, 0, or 1"""
    return (num > 0) - (num < 0)

def range_2d(width: int, height: int) -> Generator:
    for y in range(height):
        for x in range(width):
            yield (x, y)

def visible_sides(angle: int) -> Generator:
    if 0 < angle < 180: yield "left"
    if 90 < angle < 270: yield "top"
    if 180 < angle < 360: yield "right"
    if angle < 90 or angle > 270: yield "bottom"

def sublists(l: list) -> Generator:
    for sublist in l:
        for item in sublist:
            yield item

def transform_color(func: Callable, color: tuple[int, int, int]) -> tuple[int, int, int]:
    return func(color[0]), func(color[1]), func(color[2])

get_side_pixel = {
    "left": lambda mask, x, y, w, h: mask.get_at((x - 1, y)) if x > 0 else False,
    "right": lambda mask, x, y, w, h: mask.get_at((x + 1, y)) if x < w - 1 else False,
    "top": lambda mask, x, y, w, h: mask.get_at((x, y - 1)) if y > 0 else False,
    "bottom": lambda mask, x, y, w, h: mask.get_at((x, y + 1)) if y < h - 1 else False
}

# The snap function snaps a value to a central value if it enters a certain offset around the central value
@dispatch((int, float), (int, float), (int, float))
def snap(val: int | float, snap_val: int | float, offset: int | float):
    if snap_val - offset < val < snap_val + offset:
        return snap_val
    return val

# Snap for vector values
@dispatch(VEC, VEC, VEC)
def snap(val: VEC, snap_val: VEC, offset: VEC):
    if val == snap_val: return val
    val = val.copy()
    if snap_val.x - offset.x < val.x < snap_val.x + offset.x:
        val.x = snap_val.x
    if snap_val.y - offset.x < val.y < snap_val.y + offset.y:
        val.y = snap_val.y
    return val.copy()