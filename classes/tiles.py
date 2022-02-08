import pygame

from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = self.get_image(
            './assets/nature/rock_snow.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        

    def get_image(self, image: str) -> pygame.Surface:
        return pygame.transform.scale(pygame.image.load(image).convert_alpha(), (Settings().TILE_SIZE, Settings().TILE_SIZE))
