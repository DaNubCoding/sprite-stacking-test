import pygame

from constants import *

pygame.display.set_mode((100, 100))

spritesheets = {
    "car.png": pygame.image.load("car.png").convert_alpha(),
    "building.png": pygame.image.load("building.png").convert_alpha(),
    "tree.png": pygame.image.load("tree.png").convert_alpha()
}
for name, image in spritesheets.items():
    pixelarray = pygame.PixelArray(image)
    pixelarray.replace((0, 0, 0, 0), COLORKEY)
    image = pixelarray.make_surface()
    spritesheets[name] = image.convert()

pygame.display.quit()