from os.path import join, curdir
import pygame
from settings import settings
from classes.entity import Entity
from support import import_folder

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites):
        #general
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.status = 'idle'

        #praphics
        self.animation = {}
        self.import_graphics(monster_name=monster_name)
        self.image = self.animation[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        #movement
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacles_sprites = obstacle_sprites

        #stats
        self.monster_name = monster_name
        monster_info = settings.ENEMIE_DATA[monster_name]
        self.health = monster_info['HEALTH']
        self.speed = monster_info['SPEED']
        self.exp = monster_info['EXP']
        self.resistance = monster_info['RESISTANCE']
        self.attack_damage = monster_info['DAMAGE']
        self.attack_radius = monster_info['ATTACK_RADIUS']
        self.notice_radius = monster_info['NOTICE_RADIUS']
        self.attack_type = monster_info['ATTACK_TYPE']


    def get_status(self, player):
        distance = ???
        if distance <= self.attack_radius:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'


    def update(self):
        self.move(self.speed)
    
    def import_graphics(self, monster_name):
        character_path = join(curdir, 'assets', 'graphics', 'monsters', monster_name)
        
        # animation states
        self.animation = {'attack': {}, 'idle': {}, 'move': {}}                         
        for animation in self.animation.keys():
            self.animation[animation] =  import_folder(join(character_path , animation))