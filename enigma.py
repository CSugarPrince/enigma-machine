# TODO: write out full encyrption process for two
# different rotor settings.

import logging
from rotor import Rotor
from reflector import Reflector

class EnigmaMachine():
    def __init__(self):
        # Create all rotors used in a M3 Enigma machine
        self.r1 = Rotor(1, [letter for letter in "EKMFLGDQVZNTOWYHXUSPAIBRCJ"], ["Q"])
        self.r2 = Rotor(2, [letter for letter in "AJDKSIRUXBLHWTMCQGZNPYFVOE"], ["E"])
        self.r3 = Rotor(3, [letter for letter in "BDFHJLCPRTXVZNYEIWGAKMUSQO"], ["V"])
        # Store rotors in number mapped dictionary
        self.r_table = {
            1: self.r1,
            2: self.r2,
            3: self.r3
        }
        
        # plugboard
        self.plugboard = []

        # Initialize rotor sockets
        self.sockets = {
            1: self.r1,
            2: self.r2,
            3: self.r3
        }

        # Create reflectors
        self.reflectors_available = {
            "UKW-B": Reflector("UKW-B", [letter for letter in "YRUHQSLDPXNGOKMIEBFZCWVJAT"]),
            "UKW-C": Reflector("UKW-C", [letter for letter in "FVPJIAOYEDRZXWGCTKUQSBNMHL"])
        }

        self.reflector = self.reflectors_available["UKW-B"]

        self.alphabet_map = [letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


    def set_sockets(self, l):
        """ Sets sockets. l is list of rotors in ascending socket order. Ex:
        [2, 1, 3]
        sock_1 = rotor 2, 
        sock_2 = rotor 1, 
        sock_3 = rotor 3 
        """

        if not isinstance(l, list):
            raise TypeError("arg l must be a list.")
        if len(l) != 3:
            raise ValueError("len(l) must be equal to 3")
        for item in l:
            if not isinstance(item, int):
                raise ValueError("each item in l must be an integer")
            if item not in [1,2,3]:
                raise ValueError("l must contain the numbers 1,2,3")
        
        logging.debug("set_sockets() called. l is {}".format(l))
        for i in range(len(l)):
            val = l[i]
            self.sockets[i+1] = self.r_table[val] 

        logging.debug("set_sockets() finished.")
        
        # Need to reset rotors to position A
        self.reset_rotor_settings()

    
    def reset_rotor_settings(self):
        """ Resets rotor settings to setting A. """
        for i in range(3):
            self.sockets[i+1].reset_rotor()

    
    def print_sockets(self, debug=False):
        if debug:
            for k,v in self.sockets.items():
                logging.debug("sock {}: {}".format(k, str(v)))
        else:
            for s in self.sockets.values():
                print(s.type)

    def set_rotor_setting(self, sock_index, rotor_setting):
        """ Sets the rotor setting of rotor in a socket. """
        if not isinstance(sock_index, int):
            raise TypeError("sock must be an integer")        
        if sock_index not in [1, 2, 3]:
            raise ValueError("sock must be 1, 2, or 3")
        
        self.sockets[sock_index].set_setting(rotor_setting)
        


    def rotate_rotors(self):
        """ Attempts to rotate all rotors. """
        logging.debug("rotate_rotors() called.")

        # account for double stepping on middle rotor
        index = self.sockets[2].setting
        cur_set = self.alphabet_map[index]
        if cur_set in self.sockets[2].notches:
            logging.debug("Notch detected on socket 2's rotor")
            logging.info("Wheel 2 current setting {}, notch {}".format(cur_set, self.sockets[2].notches))

            logging.debug("rotating socket 2 (r{})".format(self.sockets[2].type)) # Rotate rotor 2
            self.sockets[2].rotate()
            
            logging.debug("rotating socket 1 (r{})".format(self.sockets[1].type)) # Rotate rotor 1
            self.sockets[1].rotate() 

            logging.debug("rotating socket 3 (r{})".format(self.sockets[3].type)) # Rotate rotor 3
            self.sockets[3].rotate()
            return

        # 3rd rotor always rotates. if on notch, then rotate 2nd rotor as well.
        index = self.sockets[3].setting
        cur_set = self.alphabet_map[index]
        if cur_set in self.sockets[3].notches:
            logging.info("Wheel 3 current setting {}, notch {}".format(cur_set, self.sockets[3].notches))
            logging.debug("rotating socket 3 (r{})".format(self.sockets[3].type))
            self.sockets[3].rotate()
            
            logging.debug("rotating socket 2 (r{})".format(self.sockets[2].type))
            self.sockets[2].rotate() 
            
        else:
            logging.debug("rotating socket 3 (r{})".format(self.sockets[3].type))
            self.sockets[3].rotate()


        
            
    def switch_signal(self, num):        
        let = self.alphabet_map[num]        
        pb = self.plugboard

        # Check if let has a plugboard pair
        for pair in pb:
            if let in pair:                
                # return number of letter it is paired with 
                for x in pair:
                    if x != let:
                        logging.debug("plugboard pair found {}, x is {}".format(pair, x))
                        val = self.alphabet_map.index(x)
                        return val

        # If pair not found, return original num
        logging.debug("no plugboard pair found")
        return num
        


    def step(self, num):
        """ Encrypts / Decrypts one letter. The meat of the enigma machine."""
        
        logging.debug("step() called. num is {}".format(num))

        # switch signal using plugboard
        new_num = self.switch_signal(num)
        
        # Attempt to rotate all rotors.
        self.rotate_rotors()

        # encrypt signal (input) through rotors. Signal hits third rotor first.
        out_1 = self.sockets[3].encrypt(new_num)
        out_2 = self.sockets[2].encrypt(out_1)
        out_3 = self.sockets[1].encrypt(out_2)

        # reflect signal using reflector
        out_4 = self.reflector.encrypt(out_3)

        # reflect encrypt rotors
        out_5 = self.sockets[1].backwards_encrypt(out_4)
        out_6 = self.sockets[2].backwards_encrypt(out_5)
        out_7 = self.sockets[3].backwards_encrypt(out_6)

        # switch signal on switchboard for final output.
        fin = self.switch_signal(out_7)

        # Info logs 
        logging.info("Keyboard Input: {}".format(self.alphabet_map[num]))
        logging.info("Rotors Position: {}{}{}".format(self.alphabet_map[self.sockets[1].setting], self.alphabet_map[self.sockets[2].setting], self.alphabet_map[self.sockets[3].setting] ))
        logging.info("Plugboard Encryption: {}".format(self.alphabet_map[new_num]))
        logging.info("Wheel 3 Encryption: {}".format(self.alphabet_map[out_1]))
        logging.info("Wheel 2 Encryption: {}".format(self.alphabet_map[out_2]))
        logging.info("Wheel 1 Encryption: {}".format(self.alphabet_map[out_3]))
        logging.info("Reflector Encryption: {}".format(self.alphabet_map[out_4]))
        logging.info("Wheel 1 Encryption: {}".format(self.alphabet_map[out_5]))
        logging.info("Wheel 2 Encryption: {}".format(self.alphabet_map[out_6]))
        logging.info("Wheel 3 Encryption: {}".format(self.alphabet_map[out_7]))
        logging.info("Plugboard Encryption: {}".format(self.alphabet_map[fin]))
        logging.info("Output (Lampboard): {}".format(self.alphabet_map[fin]))
        logging.info("--------------------------------------------------------------------")

        return fin



    def encrypt_msg(self, msg):
        """ Encrypts a message / string. """
        pass

    def create_plugboard_pair(self, let_1, let_2):
        """ Connect two letters on plugboard. """
        if not isinstance(let_1, str):
            raise TypeError("let_1 needs to string")
        if len(let_1) != 1:
            raise ValueError("let_1 needs to be a single character")
        if not isinstance(let_2, str):
            raise TypeError("let_2 needs to be a string")
        if len(let_2) != 1:
            raise ValueError("let_2 needs to be a single character")
        if let_1.upper() == let_2.upper():
            raise ValueError("let_1 cannot be the same as let_2")

        let_1 = let_1.upper()
        let_2 = let_2.upper()

        logging.debug("create_plugboard_pair() called")

        # If no pairs plugboard yet, just create it
        pair = (let_1, let_2)
        if self.plugboard == []:
            self.plugboard.append(pair)
            logging.debug("create_plugboard_pair() finished. pb is {}".format(self.plugboard))
            return
        
        # if (A, B) and (C, D) in pb. then func(A, C) should result in only (A, C) left.
        # if let_1 already paired in plugboard, get rid of that pair 
        old_tup = None
        for tup in self.plugboard:
            if let_1 in tup:
                index = self.plugboard.index(tup)
                old_tup = self.plugboard[index]
                self.plugboard.remove(old_tup)                

        # if let_2 already paired in plugboard, get rid of that pair            
        old_tup = None
        for tup in self.plugboard:
            if let_2 in tup:
                index = self.plugboard.index(tup)
                old_tup = self.plugboard[index]
                self.plugboard.remove(old_tup)

        self.plugboard.append(pair)

        logging.debug("create_plugboard_pair() finished. pb is {}".format(self.plugboard))




    def reset_plugboard(self):
        """ Resets plugboard. Get rid of pairs. """
        self.plugboard = []
        logging.debug("reset_plugboard() finished. pb is {}".format(self.plugboard))


if __name__ == "__main__":
    
    # Test some stuff
    logging.basicConfig(filename='enigma.log', level=logging.INFO, filemode='w')
    logging.info('Started')

    e = EnigmaMachine()

    
    # Test case 1. basic
    print("Test Case 1:")
    e.set_sockets([1,2,3])

    output = []
    for i in range(30):
        num = i % 26
        letter = e.alphabet_map[num]
        c = e.step(num)
        output.append(e.alphabet_map[c])

    # What the Letters should match
    ans = "BJELR QZVJW ARXSN BXORS TNCFM EYYAQ".replace(" ", "")
    answer = [x for x in ans]

    print(output == answer)
    

    
    # Test case 2
    print("Test Case 2:")
    e.set_sockets([2,3,1])
    e.create_plugboard_pair("A", "D")
    output = []
    for i in range(26):
        num = i % 26
        letter = e.alphabet_map[num]
        c = e.step(num)
        output.append(e.alphabet_map[c])

    # What the Letters should match
    ans = "MXYLF DHFPX AGGTE RYJRQ DEAVG W".replace(" ", "")
    answer = [x for x in ans]

    #print(output)
    #print(answer)
    print(output == answer)
    

    # Test case 3: test double stepping
    print("Test Case 3:")
    e.set_sockets([1,2,3])
    e.set_rotor_setting(2, 3) # Set socket 2's rotor to setting D
    e.reset_plugboard()
    output = []
    for i in range(26):
        num = i % 26
        letter = e.alphabet_map[num]
        c = e.step(num)
        output.append(e.alphabet_map[c])

    # What the Letters should match
    ans = "DAZIH VYGPI TMSRZ KGGHL SRBLH L".replace(" ", "")
    answer = [x for x in ans]

    print(output == answer)
    #print(answer)

    