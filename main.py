import pygame
import sys
from settings import Settings

settings = Settings()


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill('Black')

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # draw everything in the screen
            self.draw()

            # screen update
            pygame.display.update()
            self.clock.tick(settings.FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
