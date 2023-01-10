from multipledispatch import dispatch

from constants import *

def sign(num: int | float) -> int:
    """Returns the sign of the num (+/-) as -1, 0, or 1"""
    return (num > 0) - (num < 0)

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