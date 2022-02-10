import pygame
import os
from settings import *

from collections import namedtuple

settings = Settings()

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        # getting a class from json file
        __Ui = namedtuple('Ui', settings.UI.keys())
        self.data = __Ui(**settings.UI)
        
        
        #general information
        self.font = pygame.font.Font(self.data.FONT, self.data.FONT_SIZE)
        
        #bar setup
        self.health_bar_rect = pygame.Rect(
            10, 10, self.data.HEALTH_BAR_WIDTH, self.data.BAR_HEIGHT)
        
        
        self.weapon_graphics = [
            pygame.image.load(os.path.join(os.path.curdir, 'assets', 'graphics',
                         'weapons', weapon, 'full'+'.png')).convert_alpha() for weapon in settings.WEAPON_DATA.keys()]
        
        
        self.energy_bar_rect = pygame.Rect(
            10, self.data.BAR_HEIGHT + 20, self.data.ENERGY_BAR_WIDTH, self.data.BAR_HEIGHT)
        
    
    def __show_bar(self, current, max, bg_rect, color):
        #backgtound bar
        pygame.draw.rect(self.display_surface, self.data.UI_BG_COLOR, bg_rect)
        
        #drawing the bar
        ratio = current / max
        _bar_width = bg_rect.width * ratio
        _bar_rect = pygame.Rect(bg_rect.left, bg_rect.top, _bar_width, bg_rect.height)
        pygame.draw.rect(self.display_surface, color, _bar_rect)   
        pygame.draw.rect(self.display_surface, self.data.UI_BORDER_COLOR, bg_rect, 3)     
        pass

    def __show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, self.data.TEXT_COLOR)
        botright = (self.display_surface.get_width() - 20,
                   self.display_surface.get_height() - 20)
        text_rect = text_surf.get_rect(bottomright=botright)
        
        pygame.draw.rect(self.display_surface, self.data.UI_BORDER_COLOR, text_rect.inflate(20,20))
        pygame.draw.rect(self.display_surface, self.data.UI_BG_COLOR, text_rect.inflate(20,20), 3)
        
        self.display_surface.blit(text_surf, text_rect)
        pass

    def __selection_box(self, left, top, has_switched=False):
        bg_rect = pygame.Rect(left, top, self.data.ITEM_BOX_SIZE, self.data.ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, self.data.UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, self.data.UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, self.data.UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect
        
    def __weapon_overlay(self, weapon_index, has_switched=False):
        bg_rect = self.__selection_box(10, 510, has_switched)  # weapon
        weapon_surface = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surface.get_rect(center=bg_rect.center)
        
        self.display_surface.blit(weapon_surface, weapon_rect)
    
    def display(self, player):
        self.__show_bar(player.health, player.stats['health'], self.health_bar_rect, self.data.HEALTH_COLOR)
        self.__show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, self.data.ENERGY_COLOR)
        self.__show_exp(player.exp)
        self.__weapon_overlay(player.weapon_index, not player.can_switch_weapon) # weapon
