import pygame
from settings import *


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = self.get_image('./assets/eskimo/Item.png')
        self.rect = self.image.get_rect(topleft=pos)

    def get_image(self, image: str) -> pygame.Surface:
        return pygame.transform.scale(pygame.image.load(image).convert_alpha(), (Settings().TILE_SIZE, Settings().TILE_SIZE))
