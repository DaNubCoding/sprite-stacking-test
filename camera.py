from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from player import Player

from constants import *
from utils import *

class Camera:
    def __init__(self, player: Player) -> None:
        self.player = player
        self.manager = player.manager
        self.pos = self.player.pos - SIZE / 2

    def update(self) -> None:
        tick_offset = self.player.pos - self.pos - SIZE / 2
        tick_offset = snap(tick_offset, VEC(), VEC(1, 1))
        self.pos += tick_offset * 2.5 * self.manager.dt