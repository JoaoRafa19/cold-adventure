import json
from classes.singleton import *
from pprint import pprint



@singleton
class Settings:

    def __init__(self):
        self.FILE = "settings.json"
        
        self.load_settings()
    def load_settings(self):
        '''Load the game settings from a JSON file.'''
        print("Loading settings...")
        with open(self.FILE, 'r') as f:
            self.data = json.load(f)
            self.__dict__.update(self.data)
            print("Settings loaded.")
        
    def save_settings(self):
        ''' Write the game settings to a JSON file.'''
        print("Saving settings...")
        with open(self.FILE, 'w') as f:
            json.dump(self.data, f, indent=4)
            
    
    def print_settings(self):
        '''Print the game settings.'''
        for k, v in self.data.items():
            print(k + ": " + str(v))


settings = Settings()