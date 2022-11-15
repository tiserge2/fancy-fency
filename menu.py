class menu:
    def __init__(self):
        print("initializing")
        self.main_menu()

    def check_input_main_menu(self,inp):
        try:
            inp = int(inp)
            if inp < 1 or inp > 5:
                return False, "Integer must be between [0-5]"
            else: 
                return True, "All good"
        except Exception as e:
            return False, "Should be an integer"

    def main_menu(self):
        menu_text = "\n1- Start a new game\n2- Continue a saved game\n3- Change  the default scene\n4- Change the players attributes\n5- Quit\n\n"

        print(menu_text)

        choice = input("Type your choice: ")

        while not self.check_input_main_menu(choice)[0]:
            error_message = self.check_input_main_menu(choice)[1]
            print("\nError: ",error_message)
            choice = input("Type your choice: ") 
        
        print(self.main_menu_switcher(int(choice)))

    def main_menu_switcher(self,option):
        switcher = {
            1: "1",
            2: "2",
            3: "3",
            4: "4",
            5: "5"
        }

        return switcher.get(option)

menu_ = menu()