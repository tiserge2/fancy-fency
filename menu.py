import os
from environement import env
from scene import scene
from player import player
from pynput import keyboard
from datetime import datetime
from threading import Timer, Thread
import json
import re
from client import client
import time


class menu:
    def __init__(self):
        print("initializing")
        self.scenes = self.load_all_scenes()
        self.def_conf = self.load_default_conf()
        self.loaded_game = self.load_games()
        self.scene_ = None
        # Thread(target=self.main_menu).start()
        self.timer_1 = None
        self.scene_created = False
        self.player_responded = False
        self.main_menu()

    def check_input_menu(self,inp, start, end):
        try:
            inp = int(inp)
            if inp < start or inp > end:
                return False, f"Integer must be between [{start}-{end}]"
            else: 
                return True, "All good"
        except Exception as e:
            return False, "Should be an integer"

    def validate_ip_address(self, ip):
        test = re.match(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", ip)

        if not test:
            return False, "Ip Address is not correct."
        else: 
            return True, "All good"

    # different menu showing
    def main_menu(self):
        os.system("clear")
        menu_text = "\n1- Start a new game\n2- Continue a saved game\n3- Quit\n\n"

        print(menu_text)

        self.flush_input()
        choice = input("Type your choice: ")

        while not self.check_input_menu(choice, 1, 3)[0]:
            error_message = self.check_input_menu(choice,1, 3)[1]
            print("\nError: ",error_message)
            self.flush_input()
            choice = input("Type your choice: ") 
        
        self.main_menu_switcher(int(choice))

    def game_type(self):
        os.system("clear")
        menu_text = "\n1- Local\n2- Online\n3- Back\n\n\n"

        print(menu_text)

        self.flush_input()
        choice = input("Type your choice: ")

        while not self.check_input_menu(choice, 1, 3)[0]:
            error_message = self.check_input_menu(choice, 1, 3)[1]
            print("\nError: ",error_message)
            self.flush_input()
            choice = input("Type your choice: ") 
        
        self.game_type_switcher(int(choice))

    def choose_scene(self):
        os.system("clear")

        menu_text = ""
        menu_item = 0
        num_of_env = len(self.scenes)

        for i in range(num_of_env):
            menu_item += 1
            menu_text += f"\n{menu_item}- {self.scenes[i]._scene_name}"
            

        menu_text += f"\n{menu_item + 1}- Back\n\n\n"
        

        print(menu_text)

        self.flush_input()
        choice = input("Type your choice: ")

        while not self.check_input_menu(choice, 1, num_of_env + 1)[0]:
            error_message = self.check_input_menu(choice, 1, num_of_env + 1)[1]
            print("\nError: ",error_message)
            self.flush_input()
            choice = input("Type your choice: ") 

        
        self.start_game(int(choice))

    def pause_menu(self):
        os.system("clear")
        menu_text = "\n1- Save and Quit\n2- Quit without saving\n\n\n"

        print(menu_text)
        
        self.flush_input()
        choice = input("Type your choice: ")

        while not self.check_input_menu(choice, 1, 2)[0]:
            error_message = self.check_input_menu(choice,1, 2)[1]
            print("\nError: ",error_message)
            self.flush_input()
            choice = input("Type your choice: ") 
        
        self.quit_actual_game(int(choice))

    def loaded_games_menu(self):
        os.system("clear")

        menu_text = ""
        menu_item = 0
        num_of_games = len(self.loaded_game)

        if num_of_games > 0:
            for i in range(num_of_games):
                menu_item += 1
                menu_text += f"\n{menu_item}- {self.loaded_game[i]['date']}"
        else:
            menu_text = ""

        menu_text += f"\n{menu_item + 1}- Back\n\n\n"

        print(menu_text)
        
        self.flush_input()
        choice = input("Type your choice: ")

        while not self.check_input_menu(choice, 1, num_of_games + 1)[0]:
            error_message = self.check_input_menu(choice,1, num_of_games + 1)[1]
            print("\nError: ",error_message)
            self.flush_input()
            choice = input("Type your choice: ") 
        
        self.start_loaded_game(int(choice))

    def flush_input(self):
        try:
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        except ImportError:
            import sys, termios    #for linux/unix
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)

    # different menu switcher
    def quit_actual_game(self, option):
        if option == 1:
            path = "./saved_games/all_games.json"
            actual_game = {
                "date": str(datetime.now()),
                "player_1": {
                    "state": self.scene_.player_1._state,
                    "position": self.scene_.player_1._position,
                    "point": self.scene_.player_1._point,
                    "def_range": self.scene_.player_1._def_range,
                    "att_range": self.scene_.player_1._att_range,
                    "block_time": self.scene_.player_1._block_time,
                    "mvt_speed": self.scene_.player_1._mvt_speed,
                    "att_speed": self.scene_.player_1._att_speed,
                    "moving": self.scene_.player_1._moving,
                    "attacking": self.scene_.player_1._attacking,
                    "jumping": self.scene_.player_1._jumping
                },
                "player_2": {
                     "state": self.scene_.player_2._state,
                    "position": self.scene_.player_2._position,
                    "point": self.scene_.player_2._point,
                    "def_range": self.scene_.player_2._def_range,
                    "att_range": self.scene_.player_2._att_range,
                    "block_time": self.scene_.player_2._block_time,
                    "mvt_speed": self.scene_.player_2._mvt_speed,
                    "att_speed": self.scene_.player_2._att_speed,
                    "moving": self.scene_.player_2._moving,
                    "attacking": self.scene_.player_2._attacking,
                    "jumping": self.scene_.player_2._jumping
                },
                "env": {
                    "obstacles": self.scene_.env._obstacles
                }
            }
            
            if(os.path.exists(path)): 
                f = open(path)
                data = json.load(f)
                f.close()
                
                data.append(actual_game)

                with open(path, "w") as f:
                    json.dump(data, f)
            self.loaded_game = self.load_games()
   
        self.main_menu()

    def main_menu_switcher(self,option):
        switcher = {
            1: self.game_type,
            2: self.loaded_games_menu,
            3: self.exit_game
        }

        switcher[option]()

    def game_type_switcher(self, option):
        print(option)
        switcher = {
            1: self.choose_scene,
            2: self.launch_player_research,
            3: self.main_menu
        }

        switcher[option]()

    # search for players over the network
    def launch_player_research(self):
        os.system("clear")

        self.flush_input()
        ip = input("IP Address:")

        while not self.validate_ip_address(ip)[0]:
            error_message = self.validate_ip_address(ip)[1]
            os.system("clear")
            print("\nError: ",error_message)
            self.flush_input()
            ip = input("IP Address:")
        
        self.send_invite(ip)

    def send_invite(self, ip):
        print("sending invite")
        joueur_1 = client()
        joueur_1.connect((ip, 55555))

        if joueur_1.status == "CONNECTED":
            joueur_1.send(json.dumps({'type':'INVITE','message': 'INIT'}))
            
            if joueur_1.status == "SENT":
                print("Invite sent to player, waiting for answer...")
                n = 5
                while n != 0:
                    time.sleep(3)
                    print("Waiting for player to respond...")
                    n -= 1
                
                if not self.player_responded:
                    print("No response from sent invitation...")
                    time.sleep(3)
                    self.game_type()
            else:
                print("There is an error sending the invite to the player...")
                time.sleep(3)
                self.game_type()
        else:
            print("There is an error connecting to this ip")
            time.sleep(3)
            self.game_type()

    def load_games(self):
        path = "./saved_games/all_games.json"

        if(os.path.exists(path)): 
            f = open(path)
            data = json.load(f)
            f.close()

            data.sort(key=lambda x:x['date'], reverse=True)
            
            return data
        else:
            return []

    def exit_game(self):
        if self.scene_created:
            self.scene_.timer.cancel()
            exit()
        else:
            exit()

    def load_default_conf(self):
        path = "./conf/default_conf.json"

        if(os.path.exists(path)): 
            f = open(path)
            data = json.load(f)
            f.close()
            
            return data[0]

    # load all the scenes from ./all_scenes folder
    def load_all_scenes(self):
        print("loading all the scenes")
        # path to all env
        path = "./all_env"
        scenes = []

        for root, dirs, files in os.walk(path):
            for file in files:
                env_loaded = env(os.path.join(path, file))
                if env_loaded._is_correct:
                    scenes.append(env_loaded)

        return scenes

    #start the game by creating the players
    def start_game(self, choice):
        num_of_env = len(self.scenes)

        if choice > num_of_env:
            self.game_type()
        else:
            env_selected = self.scenes[choice - 1]
            env_selected._frame = self.def_conf["game"]["frame"]
            player_1 = player(position = env_selected._p_1_position, def_range = self.def_conf["player_1"]["def_range"], 
                            att_range = self.def_conf["player_1"]["att_range"], block_time = self.def_conf["player_1"]["block_time"], 
                            mvt_speed = self.def_conf["player_1"]["mvt_speed"], att_speed = self.def_conf["player_1"]["att_speed"])
            player_2 = player(position = env_selected._p_2_position, def_range = self.def_conf["player_2"]["def_range"], 
                            att_range = self.def_conf["player_2"]["att_range"], block_time = self.def_conf["player_2"]["block_time"], 
                            mvt_speed = self.def_conf["player_2"]["mvt_speed"], att_speed = self.def_conf["player_2"]["att_speed"])
            self.scene_ = scene(player_1, player_2, env_selected)
            self.scene_created = True
            self.scene_.draw_scene()
            self.keyboard_listener = keyboard.Listener(on_press = self.handle_game_pause)
            self.keyboard_listener.start()

    def start_loaded_game(self, choice):
        num_of_games = len(self.loaded_game)

        if choice > num_of_games:
            self.main_menu()
        else:
            game_selected = self.loaded_game[choice - 1]
            # we need to remove this object from the list of saved games

            
            player_1 = player(position = game_selected['player_1']['position'], def_range = game_selected["player_1"]["def_range"], 
                            att_range = game_selected["player_1"]["att_range"], block_time = game_selected["player_1"]["block_time"], 
                            mvt_speed = game_selected["player_1"]["mvt_speed"], att_speed = game_selected["player_1"]["att_speed"], 
                            point = game_selected["player_1"]["point"])
            player_2 = player(position = game_selected['player_2']['position'], def_range = game_selected["player_2"]["def_range"], 
                            att_range = game_selected["player_2"]["att_range"], block_time = game_selected["player_2"]["block_time"], 
                            mvt_speed = game_selected["player_2"]["mvt_speed"], att_speed = game_selected["player_2"]["att_speed"], 
                            point = game_selected["player_2"]["point"])

            if self.scene_created:
                self.scene_.env._obstacles = game_selected['env']['obstacles']
                self.scene_.player_1 = player_1
                self.scene_.player_2 = player_2
                self.scene_.showing = True
            else:
                env_selected = self.scenes[0]
                env_selected._frame = self.def_conf["game"]["frame"]
                self.scene_ = scene(player_1, player_2, env_selected)
                self.scene_.env._obstacles = game_selected['env']['obstacles']
                self.scene_created = True
                self.scene_.showing = True
                self.scene_.draw_scene()
                self.keyboard_listener = keyboard.Listener(on_press = self.handle_game_pause)
                self.keyboard_listener.start()
            
    def handle_game_pause(self, key):
        try:
            button = key.char
        except Exception as e:
            button = key.name
        
        if button == "t":
            self.scene_.showing = False
            self.pause_menu()
        if button == "y":
            # self.scene_.frame = 0.05
            self.scene_.showing = True

menu_ = menu()