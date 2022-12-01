from threading import Timer, Thread
import os
from pynput import keyboard
from pynput.keyboard import Controller
import time
from sound import sound
import json

class scene:
    def __init__(self, player1, player2, env, online=False, type_of_player='client', server=None, client=None):
        self.online = online
        self.type_of_player = type_of_player
        self.server = server
        self.client = client
        self.player_1 = player1
        self.player_2 = player2
        self.env = env
        self.keyboard_listener = keyboard.Listener(on_press = self.handle_input)
        self.keyboard_listener.start()
        self.win_width = 56
        self.win_height = 0
        self.message_show = False
        self.frame = env._frame
        self.showing = False
        self.show_pause_menu = False
        self.timer = None
        self.sound = sound()

    # initialise the scene drawing and control the framing
    def draw_scene(self):
        self.timer = Timer(1/self.frame, self.draw_scene)
        self.timer.start()
        """ TODO: make the clear screen work for windows also """
        if self.showing:
            if os.name == 'nt':
                os.system("cls")
            else:
                os.system("clear")
                
            self.draw_whole_env()

    # change player state based on their speed attributes
    def init_action(self, player, action, num = 0):
        if action in ["LEFT", "RIGHT", "BLOCK"]:
            player._moving = True
            delay = player._mvt_speed / self.frame
            
            time.sleep(delay)
            Thread(target=self.sound.play_sound, args=(action, )).start()
            
            if action == "LEFT":
                player._position = player._position - 1 

            if action == "RIGHT":
                player._position = player._position + 1 

            if action == "BLOCK":
                player._state = "BLOCK"

            player._moving = False
        elif action == "ATTACK":
            player._attacking = True
            delay = player._att_speed / self.frame

            time.sleep(delay)
            Thread(target=self.sound.play_sound, args=(action, )).start()

            player._state = "ATTACK"
            player._attacking = False
            self.check_touched(num)
            Thread(target=self.reinit_player, args=(player, num)).start()

    def handle_jump(self, player, way):
        player._jumping = True
        delay = player._mvt_speed / self.frame
        Thread(target=self.sound.play_sound, args=("JUMP", )).start()

        if way == "RIGHT":
            time.sleep(delay)
            player._position += 1

            time.sleep(delay)
            player._position += 1

            time.sleep(delay)
            player._position += 1
        else:
            time.sleep(delay)
            player._position -= 1

            time.sleep(delay)
            player._position -= 1

            time.sleep(delay)
            player._position -= 1

        time.sleep(delay)
        player._jumping = False

    def receive_client_input(self, server):
        while True:
            client_key = server.client_connected.recv(1024).decode()
            # similate a button touch here with pynput
            client_key = json.loads(client_key)['key']
            Thread(target = self.handle_outer_input, args = (client_key,"client")).start()

    def receive_server_input(self, joueur_1):
        while True:
            server_key = joueur_1.client_sock.recv(1024).decode()
            server_key = json.loads(server_key)['key']
            # similate a button touch here with pynput
            Thread(target = self.handle_outer_input, args = (server_key,"server")).start()

    def send_client_input(self, joueur_1, key):
        # print("send client")
        joueur_1.send(json.dumps({'type': 'GAME', 'key': key}))

    def send_server_input(self, server, key):
        # print("send client")
        server.send(json.dumps({'type': 'GAME', 'key': key}))

    def handle_outer_input(self,key, outer_player):
        button = key

        if button == "t":
            # initiate the pause for the other player
            keyboard = Controller()
            keyboard.press("t")
            keyboard.release("t")

        if outer_player == 'server':
            # ============> second player command
            if button == "left":
                # move player 2 to the left if possible
                if self.can_move(2, "LEFT") and self.player_2._moving == False:
                    Thread(target=self.init_action, args=(self.player_2, "LEFT")).start()
            elif button == "right":
                # move player 2 to the right if possible
                if self.can_move(2, "RIGHT") and self.player_2._moving == False:
                    Thread(target=self.init_action, args=(self.player_2, "RIGHT")).start()
            elif button == "p":
                # player 2 defending
                if self.player_2._state == "REST":
                    self.player_2._state = "BLOCK"
                    Thread(target=self.reinit_player, args=(self.player_2, self.player_2._block_time)).start()
            elif button == "o" and self.player_1._attacking == False:
                # player 2 attacking
                if self.player_2._state == "REST":
                    Thread(target=self.init_action, args=(self.player_2, "ATTACK", 2)).start()
            elif button == "m":
                # player 2 jumping right
                if self.can_move(2, "JUMP_RIGHT") and self.player_2._moving == False and self.player_2._jumping == False:
                    Thread(target=self.handle_jump, args=(self.player_2, "RIGHT")).start()
            elif button == "l":
                # player 2 jumping left
                if self.can_move(2, "JUMP_LEFT") and self.player_2._moving == False and self.player_2._jumping == False:
                    Thread(target=self.handle_jump, args=(self.player_2, "LEFT")).start()
        elif outer_player == 'client':
            # ============> first player command
            if button == "q" :
                # move player 1 to the the left if possible
                if self.can_move(1, "LEFT") and self.player_1._moving == False:
                    Thread(target=self.init_action, args=(self.player_1, "LEFT")).start()
            elif button == "d":
                # move player 1 to the right if possible
                if self.can_move(1, "RIGHT") and self.player_1._moving == False:
                    Thread(target=self.init_action, args=(self.player_1, "RIGHT")).start()
            elif button == "s":
                # player 1 blocking
                if self.player_1._state == "REST":
                    self.player_1._state = "BLOCK"
                    Thread(target=self.reinit_player, args=(self.player_1, self.player_2._block_time)).start()
            elif button == "z":
                # player 1 attacking
                if self.player_1._state == "REST" and self.player_1._attacking == False:
                    Thread(target=self.init_action, args=(self.player_1, "ATTACK", 1)).start()
            elif button == "e":
                # player 1 jumping right
                if self.can_move(1, "JUMP_RIGHT") and self.player_1._moving == False and self.player_1._jumping == False:
                    Thread(target=self.handle_jump, args=(self.player_1, "RIGHT")).start()
            elif button == "a":
                # player 1 jumping left
                if self.can_move(1, "JUMP_LEFT") and self.player_1._moving == False and self.player_1._jumping == False:
                    Thread(target=self.handle_jump, args=(self.player_1, "LEFT")).start()

    # control the user input when the game is playing
    def handle_input(self, key):
        try:
            button = key.char
        except Exception as e:
            button = key.name

        # print("keyboard is triggeredd:", button)
        if button == 't':
            self.showing = False
            self.show_pause_menu = True

        if self.showing:
            #here we will send the data if the game is being played online
            if self.online:
                # print("going to send input now")
                if self.type_of_player == 'client':
                    self.send_client_input(self.client, button)
                else:
                    self.send_server_input(self.server, button)
            
            if not self.online:        
                # ============> first player command
                if button == "q" :
                    # move player 1 to the the left if possible
                    if self.can_move(1, "LEFT") and self.player_1._moving == False:
                        Thread(target=self.init_action, args=(self.player_1, "LEFT")).start()
                elif button == "d":
                    # move player 1 to the right if possible
                    if self.can_move(1, "RIGHT") and self.player_1._moving == False:
                        Thread(target=self.init_action, args=(self.player_1, "RIGHT")).start()
                elif button == "s":
                    # player 1 blocking
                    if self.player_1._state == "REST":
                        self.player_1._state = "BLOCK"
                        Thread(target=self.reinit_player, args=(self.player_1, self.player_2._block_time)).start()
                elif button == "z":
                    # player 1 attacking
                    if self.player_1._state == "REST" and self.player_1._attacking == False:
                        Thread(target=self.init_action, args=(self.player_1, "ATTACK", 1)).start()
                elif button == "e":
                    # player 1 jumping right
                    if self.can_move(1, "JUMP_RIGHT") and self.player_1._moving == False and self.player_1._jumping == False:
                        Thread(target=self.handle_jump, args=(self.player_1, "RIGHT")).start()
                elif button == "a":
                    # player 1 jumping left
                    if self.can_move(1, "JUMP_LEFT") and self.player_1._moving == False and self.player_1._jumping == False:
                        Thread(target=self.handle_jump, args=(self.player_1, "LEFT")).start()
                # ============> second player command
                elif button == "left":
                    # move player 2 to the left if possible
                    if self.can_move(2, "LEFT") and self.player_2._moving == False:
                        Thread(target=self.init_action, args=(self.player_2, "LEFT")).start()
                elif button == "right":
                    # move player 2 to the right if possible
                    if self.can_move(2, "RIGHT") and self.player_2._moving == False:
                        Thread(target=self.init_action, args=(self.player_2, "RIGHT")).start()
                elif button == "p":
                    # player 2 defending
                    if self.player_2._state == "REST":
                        self.player_2._state = "BLOCK"
                        Thread(target=self.reinit_player, args=(self.player_2, self.player_2._block_time)).start()
                elif button == "o" and self.player_1._attacking == False:
                    # player 2 attacking
                    if self.player_2._state == "REST":
                        Thread(target=self.init_action, args=(self.player_2, "ATTACK", 2)).start()
                elif button == "m":
                    # player 2 jumping right
                    if self.can_move(2, "JUMP_RIGHT") and self.player_2._moving == False and self.player_2._jumping == False:
                        Thread(target=self.handle_jump, args=(self.player_2, "RIGHT")).start()
                elif button == "l":
                    # player 2 jumping left
                    if self.can_move(2, "JUMP_LEFT") and self.player_2._moving == False and self.player_2._jumping == False:
                        Thread(target=self.handle_jump, args=(self.player_2, "LEFT")).start()
            elif self.online and self.type_of_player == 'client':
                # ============> first player command
                if button == "q" :
                    # move player 1 to the the left if possible
                    if self.can_move(1, "LEFT") and self.player_1._moving == False:
                        Thread(target=self.init_action, args=(self.player_1, "LEFT")).start()
                elif button == "d":
                    # move player 1 to the right if possible
                    if self.can_move(1, "RIGHT") and self.player_1._moving == False:
                        Thread(target=self.init_action, args=(self.player_1, "RIGHT")).start()
                elif button == "s":
                    # player 1 blocking
                    if self.player_1._state == "REST":
                        self.player_1._state = "BLOCK"
                        Thread(target=self.reinit_player, args=(self.player_1, self.player_2._block_time)).start()
                elif button == "z":
                    # player 1 attacking
                    if self.player_1._state == "REST" and self.player_1._attacking == False:
                        Thread(target=self.init_action, args=(self.player_1, "ATTACK", 1)).start()
                elif button == "e":
                    # player 1 jumping right
                    if self.can_move(1, "JUMP_RIGHT") and self.player_1._moving == False and self.player_1._jumping == False:
                        Thread(target=self.handle_jump, args=(self.player_1, "RIGHT")).start()
                elif button == "a":
                    # player 1 jumping left
                    if self.can_move(1, "JUMP_LEFT") and self.player_1._moving == False and self.player_1._jumping == False:
                        Thread(target=self.handle_jump, args=(self.player_1, "LEFT")).start()
            elif self.online and  self.type_of_player == 'server':
                # ============> second player command
                if button == "left":
                    # move player 2 to the left if possible
                    if self.can_move(2, "LEFT") and self.player_2._moving == False:
                        Thread(target=self.init_action, args=(self.player_2, "LEFT")).start()
                elif button == "right":
                    # move player 2 to the right if possible
                    if self.can_move(2, "RIGHT") and self.player_2._moving == False:
                        Thread(target=self.init_action, args=(self.player_2, "RIGHT")).start()
                elif button == "p":
                    # player 2 defending
                    if self.player_2._state == "REST":
                        self.player_2._state = "BLOCK"
                        Thread(target=self.reinit_player, args=(self.player_2, self.player_2._block_time)).start()
                elif button == "o" and self.player_1._attacking == False:
                    # player 2 attacking
                    if self.player_2._state == "REST":
                        Thread(target=self.init_action, args=(self.player_2, "ATTACK", 2)).start()
                elif button == "m":
                    # player 2 jumping right
                    if self.can_move(2, "JUMP_RIGHT") and self.player_2._moving == False and self.player_2._jumping == False:
                        Thread(target=self.handle_jump, args=(self.player_2, "RIGHT")).start()
                elif button == "l":
                    # player 2 jumping left
                    if self.can_move(2, "JUMP_LEFT") and self.player_2._moving == False and self.player_2._jumping == False:
                        Thread(target=self.handle_jump, args=(self.player_2, "LEFT")).start()
                   
    # draw everything related to the game being played
    def draw_whole_env(self):
        score_board_shown = False
        characters_loading = 0
        characters_shown = False
        game_stats = False
        size = os.get_terminal_size()
        
        if size.columns < 50:
            self.win_width = 50
        else:
            self.win_width = size.columns

        if size.lines > 50:
            self.win_height = 50
        elif size.lines < 30:
            self.win_height = 30
        else:
            self.win_height = size.lines

        print(" ", "_" * (self.win_width - 2))

        characters = self.define_characters()

        for i in range(self.win_height - 4):
            percentage_win = round((i / (self.win_height)),2)
            text = ""
            text_formater = ""

            # score board showing
            if (percentage_win >= 0.15) and score_board_shown == False:
                text = f"| {self.player_1._point} | {self.player_2._point} |"
                score_board_shown = True
                text_formater = "{:^" + str((self.win_width - 9)) + "}"
            
            # drawing the players
            if (percentage_win >= 0.60) and characters_shown == False:
                characters_loading += 1
                text_formater = "{}"
                text = characters[characters_loading]
                
                if characters_loading == 6:
                    text = text.replace(" ", "_") + (self.win_width - 4 - len(text)) * "_"
                    for obs in self.env._obstacles:
                        text = text[:obs] + "X" + text[obs+1:]
                    characters_shown = True

            
            # printing everything on the line
            if text_formater != "":
                print("|", text_formater.format(text))
            else:
                print("|") 

            # printing utility debugging stuff
            debugging = False
            if not game_stats and characters_shown and debugging:
                print("\n",f"P1 => Distance: {self.player_1._position} | State: {self.player_1._state}")
                print(f"P2 => Distance: {self.player_2._position} | State: {self.player_2._state}")
                print(f"Distance 1 and 2: {self.player_2._position - self.player_1._position}")
                print(f"Obstacles: {str(self.env._obstacles)}")
                game_stats = True

    # collision detection
    def can_move(self,player, move):
        obstacles = []

        if player == 1 and move == "LEFT":
            return (self.player_1._position > 0)  and ((self.player_1._position - 1) not in self.env._obstacles)
        elif player == 1 and move == "RIGHT":
            return ((self.player_2._position - self.player_1._position) > 4) and ((self.player_1._position + 2) not in self.env._obstacles)
        elif player == 1 and move == "JUMP_LEFT":
            for i in self.env._obstacles:
                obstacles.append(i - 1)
                obstacles.append(i)
            return (self.player_1._position + 2 > 0) and ((self.player_1._position - 3) not in obstacles)
        elif player == 1 and move == "JUMP_RIGHT":
            for i in self.env._obstacles:
                obstacles.append(i - 1)
                obstacles.append(i)
            return ((self.player_2._position - (self.player_1._position + 2)) > 4) and ((self.player_1._position + 3) not in obstacles)
        elif player == 2 and move == "LEFT":
            return ((self.player_2._position - self.player_1._position) > 4) and ((self.player_2._position + 2) not in self.env._obstacles)
        elif player == 2 and move == "RIGHT":
            return (self.player_2._position < self.win_width - 9) and ((self.player_2._position + 5) not in self.env._obstacles)
        elif player == 2 and move == "JUMP_LEFT":
            for i in self.env._obstacles:
                obstacles.append(i - 1)
                obstacles.append(i)
            return ((self.player_2._position - (self.player_1._position + 2)) > 4) and ((self.player_2._position ) not in obstacles)
        elif player == 2 and move == "JUMP_RIGHT":
            for i in self.env._obstacles:
                obstacles.append(i - 3)
                obstacles.append(i - 4)
            return (self.player_2._position + 2 < self.win_width - 9) and ((self.player_2._position + 3) not in obstacles)

    # reinitialise the player state to REST
    def reinit_player(self, player, delay):
        time.sleep(delay)
        player._state = "REST"
    
    # reset the game to initial position
    def reset_game(self):
        self.player_1._position = self.env._p_1_position
        self.player_2._position = self.env._p_2_position
        self.frames_shown = 0
        self.player_1._state = "REST"
        self.player_2._state = "REST"
        Thread(target=self.sound.play_sound, args=("POINT_ADDED", )).start()

    #check if on player touch another upon attacking
    def check_touched(self, player_num):
        dist = self.player_2._position - self.player_1._position

        if player_num == 2:
            if self.player_2._att_range >= dist:
                if self.player_1._state == "REST":
                    self.player_2._point += 1
                    time.sleep(1.5)
                    # here we reinitialise the game
                    self.reset_game()
                elif self.player_1._state == "BLOCK":
                    if dist <= self.player_2.att_range - self.player_1._def_range:
                        self.player_2._point += 1
                        time.sleep(1.5)
                        # here we reinitialise the game
                        self.reset_game()
                elif self.player_1._state == "ATTACK":
                    self.reset_game()

        if player_num == 1:
            if self.player_1._att_range >= dist:
                if self.player_2._state == "REST":
                    self.player_1._point += 1
                    time.sleep(1.5)
                    # here we reinitialise the game
                    self.reset_game()
                elif self.player_2._state == "BLOCK":
                    if dist <= self.player_1.att_range - self.player_2._def_range:
                        self.player_1._point += 1
                        time.sleep(1.5)
                        # here we reinitialise the game
                        self.reset_game()
                elif self.player_2._state == "ATTACK":
                    self.reset_game()

    # create the skeleton for both players
    def define_characters(self):
        character_1 = {
            1: "<o>",
            2: ["|", " ", "|"],
            3: ["|", "_", "/", ""],
            4: "|",
            5: ["/", "|"]
        }

        character_2 = {
            1: "<o>",
            2: ["|", " ", "|"],
            3: [" ", "\\", "_", "|"],
            4: "|",
            5: ["|", "\\"]
        }

        if self.player_1._state == "BLOCK":
            character_1[3][2] = "|"
        elif self.player_1._state == "ATTACK":
            character_1[3][2] = "_"
            if (self.player_2._position - self.player_1._position) > 4:
                character_1[3][3] = "_"
            else:
                character_1[3][3] = ""
        else:
            character_1[3][2] = "/"
            character_1[3][3] = ""

        if self.player_2._state == "BLOCK":
            character_2[3][1] = "|"
        elif self.player_2._state == "ATTACK":
            character_2[3][0] = "_" 
            character_2[3][1] = "_"
        else:
            character_2[3][0] = " "
            character_2[3][1] = "\\"

        final_characters = {1: "", 2: "", 3: "", 4: "", 5: "", 6: ""}

        if self.player_1._jumping and self.player_2.jumping:
            for key in final_characters:
                if key != 6:
                    characters_loading  = key
                    first_character_pos = self.player_1._position
                    second_character_pos = self.player_2._position

                    first_character = ""
                    second_character = ""

                    if characters_loading == 2:
                        first_character = (" " * first_character_pos) + " " + character_1[characters_loading][0]
                        second_character = (" " * (second_character_pos - len(first_character))) + (" " * 3) + character_2[characters_loading][0]
                    elif characters_loading == 3:
                        first_character = (" " * first_character_pos) + " " + character_1[characters_loading][0] + character_1[characters_loading][1]  + character_1[characters_loading][2] + character_1[characters_loading][3]
                        second_character = (" " * (second_character_pos - len(first_character))) + character_2[characters_loading][0] + character_2[characters_loading][1] + character_2[characters_loading][2] + character_2[characters_loading][3]
                    elif characters_loading == 5:
                        first_character = (" " * first_character_pos) + character_1[characters_loading][0]  + character_1[characters_loading][1]
                        second_character = (" " * (second_character_pos - len(first_character))) + (" " * 3) +  character_2[characters_loading][0]  + character_2[characters_loading][1]
                    else:
                        if characters_loading == 1:
                            space_first = ""
                            space_second = " " * 2
                        else:
                            space_first = " "
                            space_second = " " * 3

                        first_character = (" " * first_character_pos) + space_first + character_1[characters_loading]
                        second_character = (" " * (second_character_pos - len(first_character))) + space_second + character_2[characters_loading]

                    text = first_character + second_character
                    final_characters[key] = text
                else:
                    final_characters[key] = (" " * (self.win_width - 9))
        elif not self.player_1._jumping and not self.player_2.jumping:
            for key in final_characters:
                if key != 1:
                    characters_loading  = key - 1
                    first_character_pos = self.player_1._position
                    second_character_pos = self.player_2._position

                    first_character = ""
                    second_character = ""

                    if characters_loading == 2:
                        first_character = (" " * first_character_pos) + " " + character_1[characters_loading][0]
                        second_character = (" " * (second_character_pos - len(first_character))) + (" " * 3) + character_2[characters_loading][0]
                    elif characters_loading == 3:
                        first_character = (" " * first_character_pos) + " " + character_1[characters_loading][0] + character_1[characters_loading][1]  + character_1[characters_loading][2] + character_1[characters_loading][3]
                        second_character = (" " * (second_character_pos - len(first_character))) + character_2[characters_loading][0] + character_2[characters_loading][1] + character_2[characters_loading][2] + character_2[characters_loading][3]
                    elif characters_loading == 5:
                        first_character = (" " * first_character_pos) + character_1[characters_loading][0]  + character_1[characters_loading][1]
                        second_character = (" " * (second_character_pos - len(first_character))) + (" " * 3) +  character_2[characters_loading][0]  + character_2[characters_loading][1]
                    else:
                        if characters_loading == 1:
                            space_first = ""
                            space_second = " " * 2
                        else:
                            space_first = " "
                            space_second = " " * 3

                        first_character = (" " * first_character_pos) + space_first + character_1[characters_loading]
                        second_character = (" " * (second_character_pos - len(first_character))) + space_second + character_2[characters_loading]

                    text = first_character + second_character
                    final_characters[key] = text
                else:
                    text = (" " * (self.win_width - 9))
                    final_characters[key] =  text
        elif self.player_1._jumping and not self.player_2.jumping:
            for key in final_characters:
                characters_loading  = key
                characters_loading_1 = characters_loading
                characters_loading_2 = characters_loading - 1
                first_character_pos = self.player_1._position
                second_character_pos = self.player_2._position

                first_character = ""
                second_character = ""

                if characters_loading == 2:
                    first_character = (" " * first_character_pos) + " " + character_1[characters_loading_1][0]
                    second_character = (" " * (second_character_pos - len(first_character))) + " " * 2 + character_2[characters_loading_2]
                elif characters_loading == 3:
                    first_character = (" " * first_character_pos) + " " + character_1[characters_loading_1][0] + character_1[characters_loading_1][1]  + character_1[characters_loading_1][2] + character_1[characters_loading_1][3]
                    second_character = (" " * (second_character_pos - len(first_character))) + (" " * 3) + character_2[characters_loading_2][0]
                elif characters_loading == 5:
                    first_character = (" " * first_character_pos) +  character_1[characters_loading_1][0]  + character_1[characters_loading_1][1]
                    second_character = (" " * (second_character_pos - len(first_character))) + " " * 3 + character_2[characters_loading_2]
                elif characters_loading == 6:
                    second_character = (" " * (second_character_pos - len(first_character))) + (" " * 3) +  character_2[characters_loading_2][0]  + character_2[characters_loading_2][1]
                else:
                    if characters_loading == 1:
                        space_first = ""
                    elif characters_loading == 4:
                        space_first = " "

                    if characters_loading_1 != 6:
                        first_character = (" " * first_character_pos) + space_first + character_1[characters_loading_1]
                    if characters_loading_2 == 3:
                        second_character = (" " * (second_character_pos - len(first_character))) + character_2[characters_loading_2][0] + character_2[characters_loading_2][1] + character_2[characters_loading_2][2] + character_2[characters_loading_2][3]

                text = first_character + second_character
                final_characters[key] = text
        elif not self.player_1._jumping and self.player_2.jumping:
            for key in final_characters:
                characters_loading  = key 
                characters_loading_1 = characters_loading - 1
                characters_loading_2 = characters_loading
                first_character_pos = self.player_1._position
                second_character_pos = self.player_2._position

                first_character = ""
                second_character = ""

                if characters_loading == 2:
                    first_character = (" " * first_character_pos) + character_1[characters_loading_1]
                    second_character = (" " * (second_character_pos - len(first_character))) + (" " * 3) + character_2[characters_loading_2][0]
                elif characters_loading == 3:
                    first_character = (" " * first_character_pos) + " " + character_1[characters_loading_1][0]
                    second_character = (" " * (second_character_pos - len(first_character))) + character_2[characters_loading_2][0] + character_2[characters_loading_2][1] + character_2[characters_loading_2][2] + character_2[characters_loading_2][3]
                elif characters_loading == 5:
                    first_character = (" " * first_character_pos) + " " + character_1[characters_loading_1]
                    second_character = (" " * (second_character_pos - len(first_character))) + (" " * 3) +  character_2[characters_loading_2][0]  + character_2[characters_loading_2][1]
                else:
                    if characters_loading == 1:
                        space_second = " " * 2
                    else:
                        space_second = " " * 3

                    if characters_loading_2 == 1:
                        second_character = (" " * (second_character_pos - len(first_character))) + space_second + character_2[characters_loading_2]
                    if characters_loading_2 == 4:
                        first_character = (" " * first_character_pos) + " " + character_1[characters_loading_1][0] + character_1[characters_loading_1][1]  + character_1[characters_loading_1][2] + character_1[characters_loading_1][3]
                        second_character = (" " * (second_character_pos - len(first_character))) + space_second + character_2[characters_loading_2]
                    if characters_loading == 6:
                        first_character = (" " * first_character_pos) +  character_1[characters_loading_1][0]  + character_1[characters_loading_1][1]

                text = first_character + second_character
                final_characters[key] = text

        return final_characters
