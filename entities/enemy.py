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

    
        #player interaction 
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 600

    def cooldown(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time > self.attack_cooldown:
                self.can_attack = True
                self.attack_time = current_time

    def get_player_distance_direction(self, player):
        ''' get the distance between the monster and the player '''
        
        # get the distance between the monster and the player
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()


        # get the direction of the player[
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return (distance, direction)

    def get_status(self, player):
        distance , direction = self.get_player_distance_direction(player)
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            print('attack')
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
            
        else:
            self.direction = pygame.math.Vector2(0, 0)

    def update(self):
        self.move(self.speed)
        self.animate()
        self.cooldown()

    def animate(self):
        animation = self.animation[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        
        self.image = self.animation[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
    
    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
    
    def import_graphics(self, monster_name):
        character_path = join(curdir, 'assets', 'graphics', 'monsters', monster_name)
        
        # animation states
        self.animation = {'attack': {}, 'idle': {}, 'move': {}}                         
        for animation in self.animation.keys():
            self.animation[animation] =  import_folder(join(character_path , animation))