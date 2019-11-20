import logging
import enigma
import cmd

class UI(cmd.Cmd):
    intro = 'Enigma Machine initialized.   Type help or ? to list commands.\n'
    prompt = '> '

    def __init__(self, file=None):
        super().__init__()
        self.enigma = enigma.EnigmaMachine()

    def do_help(self, inp):
        print("halp")

    def do_quit(self, inp):
        print("Shutting down Enigma Machine.")
        return True
    

if __name__ == "__main__":
    logging.basicConfig(filename='main.log', level=logging.DEBUG)
    logging.info('Started')
    
    # Run the Enigma Machine UI
    UI().cmdloop()


    logging.info('Finished')
