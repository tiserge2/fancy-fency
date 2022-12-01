import os

class env():
    def __init__(self, path):
        self.path = path
        self.obstacles = []
        self.player_1_position = 0
        self.player_2_position = 0
        self.scene_name = ""
        self.frame = 5
        self.is_correct = self.parse_scene()

    @property
    def _p_1_position(self):
        return self.player_1_position

    @property
    def _p_2_position(self):
        return self.player_2_position

    @property
    def _obstacles(self):
        return self.obstacles
    
    @_obstacles.setter
    def _obstacles(self, new_obstacles):
        self.obstacles = new_obstacles

    @property
    def _is_correct(self):
        return self.is_correct

    @property
    def _scene_name(self):
        return self.scene_name

    @property
    def _frame(self):
        return self.frame

    @_frame.setter
    def _frame(self, new_frame):
        self.frame = new_frame

    def parse_scene(self):
        content = ""

        # TO-DO: check if the path is correct
        if(os.path.exists(self.path)):
            with open(self.path, "r") as f:
                content = f.read()

            self.scene_name = self.path.split("/")[-1].split(".")[0]
                    
            for i in range(len(content)):
                if content[i] == "X":
                    # obstacles detected
                    self.obstacles.append(i)

                if content[i] == "1":
                    self.player_1_position = i

                if content[i] == "2":
                    self.player_2_position = i

            return True
        else:
            return False