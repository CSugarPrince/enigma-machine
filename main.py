import logging
import enigma
import cmd
import sys

class UI(cmd.Cmd):
    prompt = '> '

    def __init__(self, file=None):
        super().__init__()
        self.enigma = enigma.EnigmaMachine()
        self.alphabet = [letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        self.output = []
        print("\nEnigma Machine initialized.   Type help or ? to list commands.")
        self.display_enigma_state()
    
    def postcmd(self, stop, inp):
        self.display_enigma_state()
        self.output = []

    def display_enigma_state(self):
        # get rotor names, ringstellung, initial offset, plugboard
        rn = [x[1].name for x in self.enigma.sockets.items()]
        ring = [x[1].ringstellung for x in self.enigma.sockets.items()]
        io = [x[1].rotation_offset for x in self.enigma.sockets.items()]
        ref = self.enigma.reflector.type
        pb = self.enigma.plugboard
        lamp = "".join(self.output)

        print("\nEnigma Machine State:")
        print("Rotors in use: \t{} {} {}". format(rn[0], rn[1], rn[2]))
        print("Ringstellung: \t{}{}{}".format(ring[0], ring[1], ring[2]))
        print("Initial Offset: {}{}{}".format(io[0], io[1], io[2]))
        print("Reflector: \t{}".format(ref))
        print("Plugboard: \t{}".format(pb))
        print("\n")
        print("output: {}".format(lamp))
        print("\n")

    def do_e(self, inp):
        """ e: encrypts msg. Usage: 'e enigma' """

        # Error Check
        # strip whitespaces
        inp = inp.replace(" ", "")
        
        # converts to string successfully. no numbers, special chars
        if not inp.isalpha():
            print("Error: input must be alphabetic only")
            return
        
        # convert to upper
        msg = inp.upper()
        
        # e.encrypt_msg()
        ciphertext = self.enigma.encrypt_msg(msg)

        for i in range(len(ciphertext)):
            self.output.append(ciphertext[i])
            if i != 0 and i % 4 == 0:
                self.output.append(" ")
                

    def do_reset(self, inp):
        """ reset [optional flag]: Usage: 'reset -r' to reset rotors. 'reset -p' to reset plugboard. 'reset ' to reset both and reflector to default. """
        if len(inp) == 0:
            # reset both
            self.enigma.reset_plugboard()
            self.enigma.reset_rotor_settings()
            self.enigma.set_reflector("UKW-B")
            return
        
        
        if inp == "-r":
            # reset rotors
            self.enigma.reset_rotor_settings()

        elif inp == "-p":
            # reset plugboard
            self.enigma.reset_plugboard()
        
        else:
            print("Error: {} is not a proper flag".format(inp))
        
        

    def do_r(self, inp):
        """ Meaty Boi"""
        
        # Check for flag
        if len(inp) == 0:
            print("Error: r must have a flag")
            return
        
        args = inp.split(" ")
        

        flags = ["-a", "-c", "-so", "-sr", "-r"]
        flag = args[0]
        if flag not in flags:
            print("Error: improper flag. Flags: {}".format(flags))
            return
        
        
        if flag == "-a":
            # r -a: displays rotors available
            print("Rotor Num: Rotor Name")
            
            for tup in self.enigma.r_table.items():
                print(tup[0], ":", tup[1].name)
        
        if flag == "-c":
            # r -c [rotor num] [rotor num] [rotor num]: changes rotors used and order placed. Usage 'r -c 2 4 3'
            if len(args) != 4:
                print("Error: improper number of args. Usage: 'r -c [rotor num] [rotor num] [rotor num]' ")
                return
            
            config = args[1:]
            
            # check that each item in config is int and in range
            valid_nums = self.enigma.r_table.keys()
            for i in range(len(config)):
                if not config[i].isnumeric():
                    print("Error: arguments must be numbers")
                    return
                else:
                    x = config[i]
                    config[i] = int(x)

                if config[i] not in valid_nums:
                    print("Error: args contain an invalid Rotor Number. Check valid rotor numbers with 'r -a' ")
                    return
            

            self.enigma.set_sockets(config)            
            
        
        if flag == "-so":
            # 'r -so [rotor position] [initial offset]'
            if len(args) != 3:
                print("Error: improper number of args. Usage: 'r -so [rotor position] [initial offset]' ")
                return

            # Check that rotor position is num and valid.
            pos = args[1]
            valid_pos = self.enigma.sockets.keys()
            try:
                pos = int(pos)
            except:
                print("Error: rotor position must be a number.")
                return
            if pos not in valid_pos:
                print("Error: invalid rotor position")
                return

            # Check that initial offset is valid
            offset = args[2]
            if offset not in self.alphabet:
                print("Error: invalid initial offset. Must be capital letter")
                return

            self.enigma.set_rotor_initial_offset(pos, offset)
            

            
        if flag == "-sr":
            # 'r -sr [rotor position] [ringstellung]'
            if len(args) != 3:
                print("Error: improper number of args. Usage: 'r -sr [rotor position] [ringstellung]' ")
                return

            # Check that rotor position is num and valid.
            pos = args[1]
            valid_pos = self.enigma.sockets.keys()
            try:
                pos = int(pos)
            except:
                print("Error: rotor position must be a number.")
                return
            if pos not in valid_pos:
                print("Error: invalid rotor position")
                return

            # Check that ringstellung is valid
            ring = args[2]
            if ring not in self.alphabet:
                print("Error: invalid ringstellung. Must be capital letter")
                return

            self.enigma.set_rotor_ringstellung(pos, ring)

        
        if flag == "-r":
            # r -r [rotor position]: resets rotor. Usage: 'r -r 2'
            if len(args) != 2:
                print("Error: improper number of args. Usage: 'r -r 2' ")
                return
            
            pos = args[1]
            valid_pos = self.enigma.sockets.keys()
            try:
                pos = int(pos)
            except:
                print("Error: rotor position must be a number.")
                return
            if pos not in valid_pos:
                print("Error: invalid rotor position")
                return

            self.enigma.reset_rotor_settings(pos=pos)

        


    def do_ref(self, inp):
        """ ref: changes reflector used. Usage: 'ref UKW-C' """
        reflector_names = self.enigma.reflectors_available.keys()
        if inp not in reflector_names:
            print("Invalid reflector name. Reflector Names: {}". format(list(reflector_names)))
            return

        self.enigma.set_reflector(inp)



    def do_p(self, inp):
        """ p: create plugboard pair. Usage: 'p A B' """
        if len(inp) != 3:
            print("Error: invalid args. Usage: 'p A B' ")
            return
        
        args = inp.split(" ")       
        tup = (args[0], args[1])
        

        # Error Check
        for x in tup:
            if x not in self.alphabet:
                print("Error: arguments must be uppercase letters")
                return

        self.enigma.create_plugboard_pair(tup[0], tup[1])
        

    


    def do_quit(self, inp):
        print("Shutting down Enigma Machine.")
        sys.exit(0)
    
    def do_help(self, inp):
        print("Enigma Machine commands:")
        print("e: encrypts msg. Usage: 'e enigma'")
        print("reset [optional flag]: Usage: 'reset -r' to reset rotors. 'reset -p' to reset plugboard. 'reset ' to reset both.")


        print("\nRotor Commands:")
        print("r -a: displays rotors available. Usage 'r -a'")
        print("r -c [rotor num] [rotor num] [rotor num]: changes rotors used and order placed. Usage 'r -c 2 4 3' ")
        print("r -so [rotor position] [initial offset]: sets rotor initial offset. Usage: 'r -so 1 B'")
        print("r -sr [rotor position] [ringstellung]: sets rotor ringstellung. Usage: 'r -sr 2 F'")
        print("r -r [rotor position]: resets rotor. Usage: 'r -r 2' ")
        
        

        print("\nReflector Commands")
        print("ref: changes reflector used. Usage: 'ref UKW-C' ")

        print("\nPlugboard Commands")
        print("p: create plugboard pair. Usage: 'p A B' ")
    

if __name__ == "__main__":
    logging.basicConfig(filename='main.log', level=logging.INFO, filemode='w')
    logging.info('Started')
    
    # Run the Enigma Machine UI
    UI().cmdloop()


    logging.info('Finished')
