import pygame
from settings import settings



class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # movement

        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

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
