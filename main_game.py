from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from manager import Manager

from random import randint

from building import Building
from camera import Camera
from player import Player
from scene import Scene
from constants import *

class MainGame(Scene):
    def __init__(self, manager: Manager, previous_scene: Scene) -> None:
        super().__init__(manager, previous_scene)

        Player.create_cache()
        self.player = Player(self)
        self.camera = Camera(self.player)

        Building.create_cache()
        Building(self, (100, 100), 100)
        Building(self, (300, 150), 50)

    def update(self) -> None:
        self.camera.update()
        super().update()

    def draw(self) -> None:
        self.manager.screen.fill((30, 30, 30))
        super().draw()