import pygame
import sys
from settings import Settings
from classes.level import Level



class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (Settings().WIDTH, Settings().HEIGHT))
        pygame.display.set_caption(Settings().TITLE)
        self.clock = pygame.time.Clock()
        self.level = Level()

    def draw(self):
        self.screen.fill('Black')

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Settings().save_settings()
                sys.exit()
    
    def run(self):
        while True:
            self.eventHandler()

            # draw everything in the screen
            self.draw()
            self.level.run()

            # screen update
            pygame.display.update()
            self.clock.tick(Settings().FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
