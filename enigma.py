# TODO: write out full encyrption process for two
# different rotor settings.

import logging
from rotor import Rotor
from reflector import Reflector

class EnigmaMachine():
    def __init__(self):
        # Create all rotors used in a M3 Enigma machine
        self.r1 = Rotor("I", [letter for letter in "EKMFLGDQVZNTOWYHXUSPAIBRCJ"], ["Q"])
        self.r2 = Rotor("II", [letter for letter in "AJDKSIRUXBLHWTMCQGZNPYFVOE"], ["E"])
        self.r3 = Rotor("III", [letter for letter in "BDFHJLCPRTXVZNYEIWGAKMUSQO"], ["V"])
        self.r4 = Rotor("IV", [letter for letter in "ESOVPZJAYQUIRHXLNFTGKDCMWB"], ["J"])
        self.r5 = Rotor("V", [letter for letter in "VZBRGITYUPSDNHLXAWMJQOFECK"], ["Z"])
        # Store rotors in number mapped dictionary
        self.r_table = {
            1: self.r1,
            2: self.r2,
            3: self.r3,
            4: self.r4,
            5: self.r5
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

        self.a = [letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


    def set_reflector(self, name):
        if name not in self.reflectors_available.keys():
            raise ValueError("name must be either 'UKW-B' or 'UKW-C'")
        self.reflector = self.reflectors_available[name]

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
            if item not in [1,2,3,4,5]:
                raise ValueError("l must contain 3 of the following numbers 1,2,3,4,5")
        
        # TODO: no duplicates
        if len(l) != len(set(l)):
            raise ValueError("l cannot have any duplicates")

        for i in range(len(l)):
            val = l[i]
            self.sockets[i+1] = self.r_table[val] 
        
        
        # Need to reset rotors to position A
        self.reset_rotor_settings()

    
    def reset_rotor_settings(self):
        """ Resets rotor settings to ringstellung A, offset A. """
        for i in range(3):
            self.sockets[i+1].reset()

    
    def print_sockets(self, debug=False):
        print("print_sockets not implemented yet!")


    def set_rotor_ringstellung(self, sock_index, ringstellung):
        """ Sets rotor's ringstellung. """
        if not isinstance(sock_index, int):
            raise TypeError("sock must be an integer")        
        if sock_index not in [1, 2, 3]:
            raise ValueError("sock must be 1, 2, or 3")

        self.sockets[sock_index].set_ringstellung(ringstellung)


    def set_rotor_initial_offset(self, sock_index, offset):
        """ Sets the rotor setting of rotor in a socket. """
        if not isinstance(sock_index, int):
            raise TypeError("sock must be an integer")        
        if sock_index not in [1, 2, 3]:
            raise ValueError("sock must be 1, 2, or 3")
        
        self.sockets[sock_index].set_initial_offset(offset)
        


    def rotate_rotors(self):
        """ First step every time key is pressed. Attempt to rotate all rotors. """
        
        left_rot = self.sockets[1]
        mid_rot = self.sockets[2]
        right_rot = self.sockets[3]

        # If on middle rotor's notch. rotate all three rotors
        on_mid_rot_notch = mid_rot.rotation_offset in mid_rot.notches
        if on_mid_rot_notch:
            
            left_rot.rotate() # rotate left rotor
            mid_rot.rotate() # double-step causes middle rotor to rotate           
            right_rot.rotate() # right rotor always rotates

            return

        # If on right rotor's notch. rotate middle and right rotor
        on_right_rot_notch = right_rot.rotation_offset in right_rot.notches
        if on_right_rot_notch:
            
            mid_rot.rotate() 
            right_rot.rotate() 
        
        else:            
            right_rot.rotate()


        
            
    def switch_signal(self, letter):        
        if letter not in self.a:
            raise ValueError("letter must be uppercase alphabetical character.")        
        pb = self.plugboard

        # Check if let has a plugboard pair
        for pair in pb:
            if letter in pair:                
                # return letter it is paired with 
                for x in pair:
                    if x != letter:
                        logging.debug("plugboard pair found {}, x is {}".format(pair, x))
                        return x

        # If pair not found, return original letter
        logging.debug("no plugboard pair found")
        return letter
        
    def encrypt_msg(self, msg):
        """ Encrypts a message / string. """
        if not isinstance(msg, str):
            raise TypeError("msg must be a string")
        
        # Get rid of whitespaces
        msg = msg.replace(" ", "")
        
        cipher_text = []
        for letter in msg:
            c = self.step(letter)
            cipher_text.append(c)

        return cipher_text

    def step(self, letter):
        """ Encrypts / Decrypts one letter. The meat of the enigma machine."""
        if letter not in self.a:
            raise ValueError("letter must be uppercase alphabetical character.")
        

        # switch signal using plugboard
        new_let = self.switch_signal(letter)
        
        # Attempt to rotate all rotors.
        self.rotate_rotors()

        # encrypt signal (input) through rotors. Signal hits third rotor first.
        out_1 = self.sockets[3].encrypt(new_let)
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
        logging.info("Keyboard Input: {}".format(letter))
        logging.info("Rotors Position: {}{}{}. Ringstellung: {}{}{}".format(self.sockets[1].rotation_offset, self.sockets[2].rotation_offset, self.sockets[3].rotation_offset, self.sockets[1].ringstellung, self.sockets[2].ringstellung, self.sockets[3].ringstellung ))
        logging.info("Plugboard Encryption: {}".format(new_let))
        logging.info("Wheel 3 Encryption: {}".format(out_1))
        logging.info("Wheel 2 Encryption: {}".format(out_2))
        logging.info("Wheel 1 Encryption: {}".format(out_3))
        logging.info("Reflector Encryption: {}".format(out_4))
        logging.info("Wheel 1 Encryption: {}".format(out_5))
        logging.info("Wheel 2 Encryption: {}".format(out_6))
        logging.info("Wheel 3 Encryption: {}".format(out_7))
        logging.info("Plugboard Encryption: {}".format(fin))
        logging.info("Output (Lampboard): {}".format(fin))
        logging.info("--------------------------------------------------------------------")

        return fin



    

    def create_plugboard_pair(self, let_1, let_2):
        """ Connect two letters on plugboard. """
        if let_1 not in self.a:
            raise ValueError("let_1 must be uppercase alphabetical character.")
        if let_2 not in self.a:
            raise ValueError("let_2 must be uppercase alphabetical character.")
        if let_1 == let_2:
            raise ValueError("let_1 cannot be the same as let_2")
        if len(self.plugboard) == 10:
            raise Exception("Plugboard already has maximum of ten pairs.")
           

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

    """
    # Test case 1. basic
    print("Test Case 1:")
    e.set_sockets([1,2,3])

    output = []
    for i in range(30):
        num = i % 26
        letter = e.a[num]
        c = e.step(letter)
        output.append(c)

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
        letter = e.a[num]
        c = e.step(letter)
        output.append(c)

    # What the Letters should match
    ans = "MXYLF DHFPX AGGTE RYJRQ DEAVG W".replace(" ", "")
    answer = [x for x in ans]

    #print(output)
    #print(answer)
    print(output == answer)
    
    
    # Test case 3: test double stepping
    print("Test Case 3:")
    e.set_sockets([1,2,3])
    e.set_rotor_initial_offset(2, "D") # Set socket 2's rotor to setting D
    e.reset_plugboard()
    output = []
    for i in range(26):
        num = i % 26
        letter = e.a[num]
        c = e.step(letter)
        output.append(c)

    # What the Letters should match
    ans = "DAZIH VYGPI TMSRZ KGGHL SRBLH L".replace(" ", "")
    answer = [x for x in ans]

    print(output == answer)
    #print(answer)
    """
    
    
    # Final test case.
    out = []

    # Set sockets to Rotors I,II,III 
    # Set Reflector to UKW-C   
    # Encrypt "ABCDE"
    e.set_sockets([1,2,3])
    e.set_reflector("UKW-C")
    val = e.encrypt_msg("AB CDE")
    for x in val:
        out.append(x)
    out.append(" ")

    # Set Reflector to UKW-B
    # Change socket 1 rotor setting. Ringstellung "K", Offset "C"
    # Change socket 3 rotor setting. Ringstellung "F", Offset "H"    
    # Encrypt "FGHIJ"
    e.set_reflector("UKW-B")
    e.set_rotor_ringstellung(1, "K")
    e.set_rotor_initial_offset(1, "C")
    e.set_rotor_ringstellung(3, "F")
    e.set_rotor_initial_offset(3, "H")
    
    val = e.encrypt_msg("FGHIJ")
    for x in val:
        out.append(x)
    out.append(" ")
           

    # Change sockets to Rotors to III, IV, V
    # Encrypt "KLMNO"
    e.set_sockets([3,4,5])
    val = e.encrypt_msg("KLMNO")
    for x in val:
        out.append(x)
    out.append(" ")
        

    # Change Middle Rotor offset to J. (Double Step test)
    # Encrypt "PQRST"
    e.set_rotor_initial_offset(2, "J")
    val = e.encrypt_msg("PQRST")
    for x in val:
        out.append(x)
    out.append(" ")

    # Make Plugboard pairs (U, A), (V, D)
    # Encrypt "UVWXYZ"
    e.create_plugboard_pair("U", "A")
    e.create_plugboard_pair("V", "D")
    val = e.encrypt_msg("UVWXYZ")
    for x in val:
        out.append(x)
    

    print(out)
    
    ans = [letter for letter in "PXSVV JAXYZ FUIAH FCEIH HIXIFI"]
    print(ans)
    print(out == ans)

    # Victory at last!!!