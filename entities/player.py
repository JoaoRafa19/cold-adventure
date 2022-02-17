import pygame

from settings import *
from support import *
from os.path import join as pathjoin
from classes.entity import Entity

from collections import namedtuple

class Player(Entity):

    def __init__(self, pos, groups, obstacle_sprites, create_atack, destroy_attack, create_magic):

        super().__init__(groups)
        self.image = self.get_image(
            './assets/graphics/player/down_idle/idle_down.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-5, -26)
        
        #stats
        self.stats = {'health': 100, 'energy': 60, 'atack':10, 'magic':4, 'speed':6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

        #attack
        self.attacking = False
        self.atack_cooldown = 400
        self.atack_time = None

        # animation
        self.import_player_assets()
        
        #status
        self.status = 'down'

        self.obstacles_sprites = obstacle_sprites
        
        #atack
        self.create_atack = create_atack
        #weapon
        self.weapon_index = 0
        self.weapon = list(settings.WEAPON_DATA.keys())[self.weapon_index]
        self.destroy_attack = destroy_attack
        
        #switch weapon cooldown
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200
        
        #magic
        self.magic_index = 0
        self.magic = list(settings.MAGIC_DATA.keys())[self.magic_index]
        
        #switch magic cooldown
        self.create_magic = create_magic
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.magic_switch_cooldown = 200
        
        
    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0 and not self.attacking:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            
            if not 'attack' in self.status and not 'idle' in self.status:
                self.status = self.status + '_attack'
            else :
                self.status = self.status.replace('_idle', '_attack')    
            
        else:
            if 'attack' in self.status:
                
                self.status = self.status.replace('_attack', '_idle')
                 
    def animate(self):
        ''' player animations controll '''
        animation = self.animation[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        #set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        
    def import_player_assets(self):
        character_path = './assets/graphics/player'
        # animation states
        self.animation = {'up': [], 'down': [],
                          'left': [],
                          'right': [],
                          'right_idle': [],
                          'left_idle': [],
                          'up_idle': [],
                          'down_idle': [],
                          'right_attack': [],
                          'left_attack': [],
                          'up_attack': [],
                          'down_attack': []
                          }
        for key, value in self.animation.items():
            self.animation[key] = import_folder(pathjoin(character_path, key))  

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            

            # movement input
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0        
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            # attack input
            if keys[pygame.K_a]:
                self.create_atack()
                self.attacking = True
                self.atack_time = pygame.time.get_ticks()

            # magic input
            if keys[pygame.K_s]:
                self.attacking = True
                self.atack_time = pygame.time.get_ticks()
                magic_data = settings.MAGIC_DATA
                style = list(magic_data.keys())[self.magic_index]
                strengh = magic_data[style]['STRENGTH'] + self.stats['magic']
                cost = magic_data[style]['COST']
                self.create_magic(style=style, strengh=strengh, cost=cost)
                
                
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(settings.WEAPON_DATA.keys()) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(settings.WEAPON_DATA.keys())[self.weapon_index]
            
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_index == 0:
                    self.magic_index = 1
                else:
                    self.magic_index = 0
                self.magic = list(settings.MAGIC_DATA.keys())[
                    self.magic_index]
   
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(speed=self.speed)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.atack_time >= self.atack_cooldown:
                self.attacking = False
                self.destroy_attack()
        
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
                self.weapon_switch_time = None
        
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
                self.magic_switch_time = None

    def get_image(self, image: str) -> pygame.Surface:
        return pygame.transform.scale(pygame.image.load(image).convert_alpha(), (settings.TILE_SIZE, settings.TILE_SIZE))