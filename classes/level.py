import pygame

from classes.tiles import Tile

from classes.player import Player

from classes.weapon import Weapon

from debug import debug

from settings import Settings

from support import import_csv_layout, import_folder

from random import choice

from ui import UI


class Level:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        # sprite setup
        self.create_map()
        # attack sprites
        self.current_atack = None
        
        #user interface
        self.ui = UI()
        

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
                            Tile(pos=(x, y), groups=[
                                 self.obstacles_sprites], sprite_type=style)

                        elif style == 'grass':
                            Tile(pos=(x, y), groups=[
                                 self.visible_sprites, self.obstacles_sprites], sprite_type=style, surface=choice(graphics['grass']))

                        elif style == 'object':
                            Tile(pos=(x, y), groups=[
                                 self.visible_sprites, self.obstacles_sprites], sprite_type=style, surface=graphics['object'][int(col)])

        self.player = Player(
            (1980, 1435), 
            [self.visible_sprites], 
            obstacle_sprites=self.obstacles_sprites, 
            create_atack=self.create_atack, 
            destroy_attack=self.destroy_attack, 
            create_magic=self.create_magic
            )

    def create_atack(self):
        self.current_atack = Weapon(self.player, [self.visible_sprites])

    def create_magic(self, style, strengh, cost):
        print(style)
        print(strengh)
        print(cost)
        
        pass

    def destroy_attack(self):
        if self.current_atack:
            self.current_atack.kill()
        self.current_atack = None

    def run(self):
    	'''update the level and draw'''
    	self.display_surface.fill(color=self.ui.data.WATER_COLOR)
    	self.visible_sprites.update()
    	self.visible_sprites.custom_draw(self.player)
     
    	self.ui.display(self.player)


    
    
class YSortCameraGroup(pygame.sprite.Group):

    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()

        self.half_width = self.display_surface.get_width() // 2

        self.half_height = self.display_surface.get_height() // 2

        # create floor

        self.floor_surface = pygame.image.load("assets/ground.png").convert()

        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        # drawing the floor
        floor_offset = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset)
        # sort the sprites by y position
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
