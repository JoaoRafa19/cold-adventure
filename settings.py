import json
from classes.singleton import *

WORLD_MAP = [
    ["x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x"],
    ["x", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", "p", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", " ", "x"],
    ["x", " ", " ", "x", " ", "x", " ", "x", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", " ", "x"],
    ["x", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", " ", "x"],
    ["x", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", " ", "x"],
    ["x", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", " ", "x"],
    ["x", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", " ", "x"],
    ["x", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", "x", " ", " ", "x", "x", "x", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", "x", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", "x", " ", " ", "x", " ", " ", "x", " ", " ", "x", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x"]
]


@singleton
class Settings:

    def __init__(self):
        self.FILE = "settings.json"
        self.data = {
            "WIDTH":0,
            "HEIGHT":0,
            "FPS":0,
            "TITLE":"",
            "VERSION":"",
            "TILE_SIZE":0,
            "WORLD_MAP":WORLD_MAP,
        }
        # configuracoes
        self.HEIGHT = self.data["HEIGHT"]
        self.WIDTH = self.data["WIDTH"]
        self.FPS = self.data["FPS"]
        self.TITLE = self.data["TITLE"]
        self.VERSION = self.data["VERSION"]
        self.TILE_SIZE = self.data["TILE_SIZE"]
        self.WORLD_MAP = self.data["WORLD_MAP"]
        self.load_settings()
    def load_settings(self):
        '''Load the game settings from a JSON file.'''
        with open(self.FILE, 'r') as f:
            self.data = json.load(f)
            self.__dict__.update(self.data)
    def save_settings(self):
        ''' Write the game settings to a JSON file.'''
        with open(self.FILE, 'w') as f:
            json.dump(self.data, f, indent=4)
            
    
    def print_settings(self):
        '''Print the game settings.'''
        for k, v in self.data.items():
            print(k + ": " + str(v))