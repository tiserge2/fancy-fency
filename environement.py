import os

class env():
    def __init__(self, path):
        print("loading env")
        self.path = path
        self.parse_scene()
        # define env ground symbol, player 1 init start pos, player 2 init start pos, obstacle pos
        # define scence width

    def parse_scene(self):
        print("scene pat:")
        content = ""

        # TO-DO: check if the path is correct
        if(os.path.exists(self.path)):
            with open(self.path, "r") as f:
                content = f.read()
            
            print(content)
        else:
            print("path is not correct")

path = "./all_env/env1.ffscene"
env1 = env(path)