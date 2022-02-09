import pygame

from settings import *
from support import *
from os.path import join as pathjoin

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obstacle_sprites):

        super().__init__(groups)

        self.image = self.get_image(
            './assets/graphics/player/down_idle/idle_down.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-5, -26)

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.atack_cooldown = 400
        self.atack_time = None

        # animation
        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        
        #status
        self.status = 'down'
        

        self.obstacles_sprites = obstacle_sprites
        
    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    # overwrite idle status
                    self.status.replace('_idle', '_attack')
                else: 
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status.replace('_attack', '')
        
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
        if keys[pygame.K_a] and not self.attacking:
            print('attack')
            self.attacking = True
            self.atack_time = pygame.time.get_ticks()

        # magic input
        if keys[pygame.K_s] and not self.attacking:
            self.attacking = True
            self.atack_time = pygame.time.get_ticks()
            print('special')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprites in self.obstacles_sprites:
                if sprites.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprites.hitbox.left
                    elif self.direction.x < 0:  # moving left
                        self.hitbox.left = sprites.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision(direction='horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision(direction='vertical')
        self.rect.center = self.hitbox.center

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

    def get_image(self, image: str) -> pygame.Surface:
        return pygame.transform.scale(pygame.image.load(image).convert_alpha(), (Settings().TILE_SIZE, Settings().TILE_SIZE))
