from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from manager import Manager

from random import randint

from sprite import SortedSpriteManager
from profiling import profile
from building import Building
from camera import Camera
from player import Player
from scene import Scene
from constants import *
from tree import Tree

class MainGame(Scene):
    def __init__(self, manager: Manager, previous_scene: Scene) -> None:
        super().__init__(manager, previous_scene, SortedSpriteManager)

        Player.create_cache(self.manager.screen)
        self.player = Player(self)
        self.camera = Camera(self.player)

        Building.create_cache(self.manager.screen)
        for x in range(-3000, 3001, 400):
            for y in range(-3000, 3001, 400):
                Building(self, (x + randint(-80, 80), y + randint(-80, 80)), randint(0, 359))

        Tree.create_cache(self.manager.screen)
        for x in range(-3000 - 200, 3001 - 200, 400):
            for y in range(-3000 - 200, 3001 - 200, 400):
                Tree(self, (x + randint(-80, 80), y + randint(-80, 80)), randint(0, 359))

    def update(self) -> None:
        self.camera.update()
        super().update()

    def draw(self) -> None:
        self.manager.screen.clear()
        super().draw()