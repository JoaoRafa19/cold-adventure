import json
from classes.singleton import *



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
        }
        # configuracoes
        self.HEIGHT = self.data["HEIGHT"]
        self.WIDTH = self.data["WIDTH"]
        self.FPS = self.data["FPS"]
        self.TITLE:str = self.data["TITLE"]
        self.VERSION:str = self.data["VERSION"]
        self.TILE_SIZE:int = self.data["TILE_SIZE"]
        self.load_settings()
    def load_settings(self):
        '''Load the game settings from a JSON file.'''
        print("Loading settings...")
        with open(self.FILE, 'r') as f:
            self.data = json.load(f)
            self.__dict__.update(self.data)
    def save_settings(self):
        ''' Write the game settings to a JSON file.'''
        print("Saving settings...")
        with open(self.FILE, 'w') as f:
            json.dump(self.data, f, indent=4)
            
    
    def print_settings(self):
        '''Print the game settings.'''
        for k, v in self.data.items():
            print(k + ": " + str(v))