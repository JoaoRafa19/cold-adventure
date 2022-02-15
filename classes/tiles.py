import pygame

from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type: str, surface = pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface  
        if sprite_type == 'object':
            # create a offset for the object
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - settings.TILE_SIZE))
            self.hitbox = self.rect.inflate(-20, -settings.TILE_SIZE-30)
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-5, -10)
        