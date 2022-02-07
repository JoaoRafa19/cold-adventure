import pygame
from settings import WORLD_MAP, Settings
from classes.tiles import Tile
from classes.player import Player


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # sprite group setup

        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def draw(self):
        self.visible_sprites.draw(self.display_surface)

    def create_map(self):
        ''' create map from WORLD_MAP '''
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * Settings().TILE_SIZE
                y = row_index * Settings().TILE_SIZE
                if col == 'x':
                    # rock
                    tile = Tile(
                        (x, y), [self.visible_sprites, self.obstacles_sprites])
                if col == 'p':
                    player = Player(
                        (x, y), [self.visible_sprites])

    def run(self):
        #update and draw
        self.draw()

        pass
