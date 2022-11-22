from threading import Timer, Thread
import os
from pynput import keyboard
from player import player 
from getch import getch
import time

class scene:
    def __init__(self, player1, player2, env):
        self.player_1 = player1
        self.player_2 = player2
        self.draw_scene()
        self.keyboard_listener = keyboard.Listener(on_press = self.handle_input)
        self.keyboard_listener.start()
        self.win_width = 0
        self.win_height = 0
        self.message_show = False
    
    # initialise the scene drawing and control the framing
    def draw_scene(self):
        Timer(2, self.draw_scene).start()
        """ TODO: make the clear screen work for windows also """
        os.system("clear")
        self.draw_whole_env()

    # control the user input when the game is playing
    def handle_input(self, key):
        try:
            button = key.char
        except Exception as e:
            button = key.name

        # ============> first player command
        if button == "a":
            # move player 1 to the the left if possible
            if self.can_move(1, "LEFT"):
                self.player_1._position = self.player_1._position - 1
        elif button == "d":
            # move player 1 to the right if possible
            if self.can_move(1, "RIGHT"):
                self.player_1._position = self.player_1._position + 1
        elif button == "s":
            # player 1 blocking
            if self.player_1._state == "REST":
                self.player_1._state = "BLOCK"
                Thread(target=self.reinit_player, args=(self.player_1, self.player_2._block_time)).start()
        elif button == "w":
            #player 1 attacking
            if self.player_1._state == "REST":
                self.player_1._state = "ATTACK"
                self.check_touched(1)
                Thread(target=self.reinit_player, args=(self.player_1, 1)).start()
        # elif button == "q":
        #     print(f"{button} is pressed")
        # elif button == "e":
        #     print(f"{button} is pressed")
        # ============> second player command
        elif button == "left":
            # move player 2 to the left if possible
            if self.can_move(2, "LEFT"):
                self.player_2._position = self.player_2._position - 1
        elif button == "right":
            # move player 2 to the right if possible
            if self.can_move(2, "RIGHT"):
                self.player_2._position = self.player_2._position + 1
        elif button == "k":
            # player 2 defending
            if self.player_2._state == "REST":
                self.player_2._state = "BLOCK"
                Thread(target=self.reinit_player, args=(self.player_2, self.player_2._block_time)).start()
        elif button == "l":
            # player 2 attacking
            if self.player_2._state == "REST":
                self.player_2._state = "ATTACK"
                self.check_touched(2)
                Thread(target=self.reinit_player, args=(self.player_2, 1)).start()
        # elif button == "<"
        #     print(f"{button} is pressed")
        # elif button == ">":
        #     print(f"{button} is pressed")

    # draw everything related to the game being played
    def draw_whole_env(self):
        score_board_shown = False
        characters_loading = 0
        characters_shown = False
        ground_shown = False
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


        for i in range(self.win_height - 4):
            percentage_win = round((i / (self.win_height)),2)
            text = ""
            text_formater = ""

            # score board showing
            if (percentage_win >= 0.15) and score_board_shown == False:
                text = f"| {self.player_1._point} | {self.player_2._point} |"
                score_board_shown = True
                text_formater = "{:^" + str((self.win_width - 1)) + "}"

            # ground drawing
            if characters_shown and not ground_shown:
                text = (self.win_width - 4) * "#"
                text_formater = "{}"
                ground_shown = True
            
            # drawing the players
            if (percentage_win >= 0.60) and characters_shown == False:
                characters_loading += 1
                text_formater = "{}"
                first_character_pos = player_1._position
                second_character_pos = player_2._position

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
                
                if characters_loading == 5:
                    characters_shown = True
            
            # printing everything on the line
            if text_formater != "":
                print("|", text_formater.format(text))
            else:
                print("|") 
    
    # collision detection
    def can_move(self,player, move):
        if player == 1 and move == "LEFT":
            return self.player_1._position > 0
        elif player == 1 and move == "RIGHT":
            return (self.player_2._position - self.player_1._position) > 4
        elif player == 1 and move == "JUMP_LEFT":
            print("trying to move")
        elif player == 1 and move == "JUMP_RIGHT":
            print("trying to move")    
        elif player == 2 and move == "LEFT":
            return (self.player_2._position - self.player_1._position) > 4
        elif player == 2 and move == "RIGHT":
            return self.player_2._position < self.win_width - 9
        elif player == 2 and move == "JUMP_LEFT":
            print("trying to move")
        elif player == 2 and move == "JUMP_RIGHT":
            print("trying to move")

    # reinitialise the player state to REST
    def reinit_player(self, player, delay):
        time.sleep(delay)
        player._state = "REST"
    
    # reset the game to initial position
    def reset_game(self):
        self.player_1._position = 0
        self.player_2._position = 12
        self.player_1._state = "REST"
        self.player_2._state = "REST"

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
                    if player_2.att_range > player_1._def_range:
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
                    if player_1.att_range > player_2._def_range:
                        self.player_1._point += 1
                        time.sleep(1.5)
                        # here we reinitialise the game
                        self.reset_game()
                elif self.player_2._state == "ATTACK":
                    self.reset_game()


player_1 = player("REST", 0, 2, 6, 2)
player_2 = player("REST", 12, 0, 4, 2)
scene_1 = scene(player_1, player_2, 3)