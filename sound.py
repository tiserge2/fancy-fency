from pygame import mixer
import time
import os
import json

class sound():
    def __init__(self):
        mixer.init()
        self.mapping = self.load_mapping()

    def load_mapping(self):
        path = "./ressources/sound_mapping.json"

        if(os.path.exists(path)): 
            f = open(path)
            data = json.load(f)
            f.close()
            print(data)
            return data[0]

    def play_sound(self, action):
        file = "./ressources/sound_effect/" + self.mapping[action]
        if os.path.exists(file):
            try:
                sound_effect = mixer.Sound(file)
                sound_effect.play()
                time.sleep(3)
            except Exception as e:
                print("there is an issue")
        else:
            print("not exist")