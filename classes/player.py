import pygame

from settings import *


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obstacle_sprites):

        super().__init__(groups)

        self.image = self.get_image('./assets/eskimo/Item.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.obstacles_sprites = obstacle_sprites
        self.hitbox = self.rect.inflate(-5,-26)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

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
        self.move(speed=self.speed)

    def get_image(self, image: str) -> pygame.Surface:
        return pygame.transform.scale(pygame.image.load(image).convert_alpha(), (Settings().TILE_SIZE, Settings().TILE_SIZE))
