import pygame
from settings import WORLD_MAP, Settings
from classes.tiles import Tile
from classes.player import Player


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # sprite group setup

        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        # sprite setup
        self.create_map()

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
                    self.player = Player(
                        (x, y), [self.visible_sprites], obstacle_sprites=self.obstacles_sprites)

    def run(self):
        #update and draw
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player)

        pass

class YSortCameraGroup(pygame.sprite.Group):
    
    def __init__(self):
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2

    def custom_draw(self, player):
        
        # getting the offset 
        self.offset.x =  player.rect.centerx -  self.half_width
        self.offset.y =  player.rect.centery - self.half_height
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos) 