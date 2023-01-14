from pygame.locals import *
from enum import Enum
import pygame
import sys

from main_game import MainGame
from constants import *

class AbortScene(Exception):
    def __str__(self):
        return "Scene aborted but not caught with a try/except block."

class Manager:
    def __init__(self) -> None:
        self.FLAGS = DOUBLEBUF | SCALED | RESIZABLE

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), self.FLAGS)
        self.clock = pygame.time.Clock()

        self.scene = MainGame(self, None)
        self.debug = False

    def run(self) -> None:
        while True:
            self.dt = self.clock.tick_busy_loop(FPS) * 0.001
            self.update()
            try:
                self.scene.update()
                self.scene.draw()
            except AbortScene:
                continue
            pygame.display.flip()

    def update(self) -> None:
        pygame.display.set_caption(f"Sprite Stacking Game | {round(self.clock.get_fps())}")

        self.events = {event.type: event for event in pygame.event.get()}
        self.key_downs = {event.key: event for event in self.events.values() if event.type == KEYDOWN}
        self.key_ups = {event.key: event for event in self.events.values() if event.type == KEYUP}
        self.key_presses = pygame.key.get_pressed()

        if QUIT in self.events:
            self.quit()
        elif K_F3 in self.key_downs:
            self.debug = not self.debug

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def new_scene(self, scene_class: str) -> None:
        self.scene = self.Scenes[scene_class].value(self, self.scene)
        raise AbortScene

    class Scenes(Enum):
        MainGame = MainGame