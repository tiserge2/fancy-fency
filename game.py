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
from server import server


class game:
    def __init__(self):
        self.scenes = self.load_all_scenes()
        self.def_conf = self.load_default_conf()
        self.loaded_game = self.load_games()
        self.scene_ = None
        self.timer_1 = None
        self.scene_created = False
        self.player_responded = False
        self.server = server()
        self.joueur_1 = client()
        self.online_game = False
        self.online_player_type = ""
        print("Initializing the kernel...")
        print("server has connection: ", self.server.has_connection)
        time.sleep(2)
        Thread(target=self.main_menu).start()
        if self.server.has_connection:
            self.server.start_server()

    # check if the user want to pause the game
    def check_if_pause(self):
        if self.scene_.show_pause_menu:
            self.pause_menu()

    # validate the input from the menus
    def check_input_menu(self,inp, start, end):
        try:
            inp = int(inp)
            if inp < start or inp > end:
                return False, f"Integer must be between [{start}-{end}]"
            else: 
                return True, "All good"
        except Exception as e:
            return False, "Should be an integer"

    # check if the ip entered is correct or if the user want to go back
    def validate_ip_address(self, address):
        test = re.match(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]+$", address) or address == "1"

        if not test:
            return False, "Ip Address is not correct."
        else: 
            return True, "All good"

    # different menu showing
    def main_menu(self):
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")

        menu_text = "\n1- Start a new game\n2- Continue a saved game\n3- Quit\n\n"

        if type(self.server) != str:
            menu_text += f"Player Online Address: {self.server.address[0]}:{self.server.address[1]}\n\n"

        print(menu_text)

        self.flush_input()
        choice = input("Type your choice: ")

        while not self.check_input_menu(choice, 1, 3)[0]:
            error_message = self.check_input_menu(choice,1, 3)[1]
            print("\nError: ",error_message)
            self.flush_input()
            choice = input("Type your choice: ") 
        
        self.main_menu_switcher(int(choice))

    # choose between online and offline playing
    def game_type(self):
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")

        if self.server.server_state != "NEW_INVITE":
            if self.server.has_connection:
                menu_text = "\n1- Local\n2- Online\n3- Back\n\n\n"
            else:
                menu_text = "\n1- Local\n3- Back\n\n\n"


            print(menu_text)

            self.flush_input()
            choice = input("Type your choice: ")

            while not self.check_input_menu(choice, 1, 3)[0]:
                error_message = self.check_input_menu(choice, 1, 3)[1]
                print("\nError: ",error_message)
                self.flush_input()
                choice = input("Type your choice: ") 
            
            if not self.server.has_connection and int(choice) == 2:
                self.game_type()
            else:
                self.game_type_switcher(int(choice))
        else:
            menu_text = "You've got a new invitation to play.\n\n\n"

            menu_text += "\n1- Yes\n2- No\n\n\n"

            print(menu_text)

            self.flush_input()
            choice = input("Type your choice: ")

            while not self.check_input_menu(choice, 1, 2)[0]:
                error_message = self.check_input_menu(choice, 1, 3)[1]
                print("\nError: ",error_message)
                self.flush_input()
                choice = input("Type your choice: ") 
        
            self.online_game_type_switcher(int(choice))

    # choose which scenes to load
    def choose_scene(self):
        if os.name == 'nt':
            os.system("cls")
        else:
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

    # menu to show when the pause is asked in the game
    def pause_menu(self):
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")

        menu_text = "Game Control\n\nPlayer 1:\n\nq => Move Left,\nd => Move Right,\na => Jump Left,\ne => Jump Right,\nz => Attack,\ns => Block\n\n"
        menu_text += "Player 2:\n\nLeft Arrow => Move Left,\nRight Arrow => Move Right,\nl => Jump Left,\nm => Jump Right,\no => Attack,\np => Block\n\n\n"

        menu_text += "1- Save and Quit\n2- Quit without saving\n3- Resume\n\n\n"

        print(menu_text)
        
        self.flush_input()
        choice = input("Type your choice: ")

        while not self.check_input_menu(choice, 1, 3)[0]:
            error_message = self.check_input_menu(choice,1, 3)[1]
            print("\nError: ",error_message)
            self.flush_input()
            choice = input("Type your choice: ") 
        
        self.quit_actual_game(int(choice))

    # choose between the saved games which one to continue
    def loaded_games_menu(self):
        if os.name == 'nt':
            os.system("cls")
        else:
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

    # fix issue when getting user input, and we have data in instream
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
            path = "./ressources/saved_games/all_games.json"
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
        elif option == 3:
            self.scene_.showing = True
            self.scene_.show_pause_menu = False
        else:
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

    def online_game_type_switcher(self, option):
        print("responding to ", self.server.client_address)

        if option == 1:
            print("accepting")
            self.server.send(json.dumps({'type':'INVITE', 'message':'YES'}))
            if self.server.status == 'SENT':
                print("Response sent successfully.")
                # here we will launch the game for player 2
                self.start_online_game("server")
            else:
                print("Failed to send response.")
                time.sleep(2)
                self.game_type()
        else:
            print("refusing")
            self.server.send(json.dumps({'type':'INVITE', 'message':'NO'}))
            if self.server.status == 'SENT':
                print("Response sent successfully.")
                time.sleep(3)
                self.main_menu()
            else:
                print("!! Failed to send response.")
            time.sleep(3)
            self.game_type()

    # search for players over the network
    def launch_player_research(self):
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")

        self.flush_input()
        address = input("Player Address(IP:PORT) or 1 to return: ")

        while not self.validate_ip_address(address)[0]:
            error_message = self.validate_ip_address(address)[1]
            if os.name == 'nt':
                os.system("cls")
            else:
                os.system("clear")

            print("Error: ",error_message)
            self.flush_input()
            address = input("Player Address(IP:PORT) or 1 to return: ")
        
        self.send_invite(address)

    # ask online player to join for a game
    def send_invite(self, address):
        if address != "1":
            print("\nTrying to reach the please. Please wait...")
            self.joueur_1.connect((address.split(":")[0], int(address.split(":")[1])))

            if self.joueur_1.status == "CONNECTED":
                self.joueur_1.send(json.dumps({'type':'INVITE','message': 'INIT'}))
                
                if self.joueur_1.status == "SENT":
                    print("Invite sent to player, waiting for answer...")

                    try:
                        data = self.joueur_1.client_sock.recv(2048).decode()
                        data = json.loads(data)
                        self.player_responded = True
                        response = data['message']
                    except Exception as e:
                        response = "NO"

                    if not self.player_responded:
                        print("No response from sent invitation...")
                        time.sleep(3)
                        self.game_type()
                    else:
                        print("Checking player response...")
                        if response == "YES":
                            print("Invite was accepted.")
                            # here we start the game for player 1
                            self.start_online_game("client")
                        else:
                            print("Invite was refused.")
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
        else:
            self.game_type()

    # load saved games from the json file
    def load_games(self):
        path = "./ressources/saved_games/all_games.json"

        if(os.path.exists(path)): 
            f = open(path)
            data = json.load(f)
            f.close()

            data.sort(key=lambda x:x['date'], reverse=True)
            
            return data
        else:
            return []

    # exit entirely from the program
    def exit_game(self):
        print("Exiting game! See you...")
        self.server.server_sock.close()
        if self.scene_created:
            self.scene_.timer.cancel()
        
        os._exit(0)

    # load the configuration about the scenes
    def load_default_conf(self):
        path = "./ressources/conf/default_conf.json"

        if(os.path.exists(path)): 
            f = open(path)
            data = json.load(f)
            f.close()
            
            return data[0]

    # load all the scenes from ./ressources/all_scenes folder
    def load_all_scenes(self):
        print("Loading all the scenes")
        # path to all env
        path = "./ressources/all_env"
        scenes = []
        files_ = []

        for root, dirs, files in os.walk(path):
            files_ = files

        files_.sort()

        for file in files_:
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
            print("Scene name loaded: ", self.scene_.env._scene_name)
            if self.online_game:
                self.scene_.online = True
                self.scene_.server = self.server
                self.scene_.client = self.joueur_1
            self.scene_.draw_scene()
            self.scene_.showing = True
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
                # self.keyboard_listener = keyboard.Listener(on_press = self.handle_game_pause)
                self.keyboard_listener.start()
            
    def handle_game_pause(self, key):
        try:
            button = key.char
        except Exception as e:
            button = key.name
        
        if button == "t":
            # here we need to pause the game also for the other player
            self.scene_.showing = False
            self.pause_menu()

    def start_online_game(self, type):
        self.online_game = True
        self.start_game(1)
        if type == 'client':
            self.online_player_type = 'client'
            self.scene_.type_of_player = self.online_player_type
            Thread(target = self.scene_.receive_server_input, args=(self.joueur_1, )).start()
        else:
            self.online_player_type = 'server'
            self.scene_.type_of_player = self.online_player_type
            Thread(target = self.scene_.receive_client_input, args=(self.server, )).start()
