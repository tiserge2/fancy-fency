from pygame import mixer
import os

class sound():
    def __init__(self):
        mixer.init()

    def play_sound(self, file):
        if os.path.exists(file):
            mixer.music.load(file)
            mixer.music.set_volume(0.9)
            mixer.music.play()
        else:
            print("not exist")

s = sound()
s.play_sound("/Users/sergiosuzerainosson/Documents/project/universite_project/programmation_avancee/fancy-fency/ressources/sound_effect/fatality.mp3")