from pynput import keyboard

def handle_input(key):
    print("la touche presse est: ", key)


if __name__ == "__main__":
    keyboard_ = keyboard.Controller()
    keyboard.Listener(on_press = handle_input).start()
    key = "a"
    keyboard_.press(key)
    keyboard_.release(key)