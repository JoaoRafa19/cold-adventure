import pygame
from settings import Settings
from classes.tiles import Tile
from classes.player import Player
from support import import_csv_layout, import_folder
from random import choice

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # sprite group setup

        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        # sprite setup
        self.create_map()

    def create_map(self):
        ''' create map from csv file '''
        layouts = {
            'boundary': import_csv_layout('./assets/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('./assets/map/map_Grass.csv'),
            'object': import_csv_layout('./assets/map/map_Objects.csv'),
        }
        
        graphics = {
            'grass': import_folder('./assets/graphics/grass'),
            'object': import_folder('./assets/graphics/objects'),
        }
        
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * Settings().TILE_SIZE
                        y = row_index * Settings().TILE_SIZE
                        if style == 'boundary':
                            Tile(pos=(x, y), groups=[self.obstacles_sprites], sprite_type=style)
                        elif style == 'grass': 
                            Tile(pos=(x, y), groups=[
                                 self.visible_sprites, self.obstacles_sprites], sprite_type=style, surface=choice(graphics['grass']))
                        elif style == 'object':
                            Tile(pos=(x, y), groups=[self.visible_sprites, self.obstacles_sprites], sprite_type=style, surface=graphics['object'][int(col)])
        self.player = Player(
                        (1980, 1435), [self.visible_sprites], obstacle_sprites=self.obstacles_sprites)

    def run(self):
        #update and draw
        self.display_surface.fill(color=(0, 0, 100))
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
        
        #create floor
        self.floor_surface = pygame.image.load("assets/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0,0))
        

    def custom_draw(self, player):
        
        
        
        # getting the offset 
        
        self.offset.x =  player.rect.centerx -  self.half_width
        
        self.offset.y =  player.rect.centery - self.half_height
        
        # drawing the floor
        floor_offset = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset)
        
        # sort the sprites by y position
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos) 