from csv import reader
from os import walk
from os.path import join as pathjoin
import pygame

def import_csv_layout(path:str):
    terrain_map = []
    with open(path, 'r') as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path:str) :
    surface_list = []
    for _,__, data in walk(path):
        for image in data:
            full_path = pathjoin(path, image)
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    return surface_list
   