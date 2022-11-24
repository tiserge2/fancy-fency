import os

class env():
    def __init__(self, path):
        self.path = path
        self.obstacles = []
        self.player_1_position = 0
        self.player_2_position = 0
        self.is_correct = self.parse_scene()
        # define env ground symbol, player 1 init start pos, player 2 init start pos, obstacle pos
        # define scence width

    @property
    def _p_1_position(self):
        return self.player_1_position

    @property
    def _p_2_position(self):
        return self.player_2_position

    @property
    def _obstacles(self):
        return self.obstacles

    def parse_scene(self):
        content = ""

        # TO-DO: check if the path is correct
        if(os.path.exists(self.path)):
            with open(self.path, "r") as f:
                content = f.read()
            
            for i in range(len(content)):
                if content[i] == "X":
                    # obstacles detected
                    self.obstacles.append(i)

                if content[i] == "1":
                    self.player_1_position = i

                if content[i] == "2":
                    self.player_2_position = i

            return self.player_1_position != 0 and self.player_2_position != 0
        else:
            return False

path = "./all_env/env1.ffscene"
env1 = env(path)
print(env1.is_correct)