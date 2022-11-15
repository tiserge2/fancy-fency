from threading import Timer
import os
from pynput import keyboard

class scene:
    def __init__(self, player1, player2, env):
        self.draw_scene()
        self.keyboard_listener = keyboard.Listener(on_press = self.handle_input)
        self.keyboard_listener.start()
        

    def draw_scene(self):
        Timer(0.5, self.draw_scene).start()
        """ TODO: make the clear screen work for windows also """
        os.system("clear")
        self.draw_whole_env()

    def handle_input(self, key):
        try:
            button = key.char
        except Exception as e:
            button = key.name

        # first player command
        if button == "a":
            print(f"{button} is pressed")
        elif button == "s":
            print(f"{button} is pressed")
        elif button == "d":
            print(f"{button} is pressed")
        elif button == "q":
            print(f"{button} is pressed")
        elif button == "w":
            print(f"{button} is pressed")
        elif button == "e":
            print(f"{button} is pressed")
        # second player command
        elif button == "<":
            print(f"{button} is pressed")
        elif button == ">":
            print(f"{button} is pressed")
        elif button == "k":
            print(f"{button} is pressed")
        elif button == "l":
            print(f"{button} is pressed")
        elif button == "K_LEFT":
            print(f"{button} is pressed")
        elif button == "K_RIGHT":
            print(f"{button} is pressed")
        # pause the game
        else:
            print(f"{button} is pressed")
            
    def draw_whole_env(self):
        message_shown = False
        score_board_shown = False
        characters_shown = False
        size = os.get_terminal_size()
        win_width = size.columns
        win_height = size.lines
        print(" ", "_" * (win_width - 2))

        for i in range(win_height - 2):
            percentage_win = round((i / (win_height)),2)
            text = ""
            text_formater = ""
            # score board showing
            if (percentage_win >= 0.15) and score_board_shown == False:
                text = "| 0 | 0 |"
                score_board_shown = True
                text_formater = "{:^" + str((win_width - 1)) + "}"

            if (percentage_win >= 0.60) and characters_shown == False:
                # drawing the characters
                print("")
            
            if text_formater != "":
                print(percentage_win, text_formater.format(text))
            else:
                print(percentage_win)
                

scene_1 = scene(1, 2, 3)
