from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scene import Scene

from stacked_sprite import StackedSprite
from sprite import Layers
from constants import *
from utils import *

class Tree(StackedSprite):
    _res = "tree.png"
    _size = VEC(26, 24)
    _frames = 40
    _pixel = 6
    _pivot_offset = VEC(0, 1)

    def __init__(self, scene: Scene, pos: tuple[int, int], rot: int) -> None:
        super().__init__(scene, Layers.WORLD, pos, rot)