import logging

class Rotor():

    def __init__(self, rtype, contact_map, notches):
        """ Creates rotor. """
        if not isinstance(contact_map, list):
            raise TypeError("contact_map must be list")
        if not isinstance(notches, list):
            raise TypeError("notches must be list")

        logging.debug("Initializing rotor.")

        # Used in other methods
        self.alphabet_map = [letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

        self.type = rtype
        
        # convert letters to numbers 0-25
        self.contact_map = [self.alphabet_map.index(let) for let in contact_map]
                
        self.notches = notches       

        self.setting = 0

              
        

    def rotate(self):
        logging.debug("Before: {}".format(self.alphabet_map[self.setting]))

        # Rotates rotor once
        self.setting = (self.setting + 1) % 26

        logging.debug("After: {}".format(self.alphabet_map[self.setting]))

       
    def set_setting(self, num):
        if not isinstance(num, int):
            raise TypeError("arg num must be an int.")
        if num < 0 or num > 25:
            raise ValueError("num must between 0 and 25 inclusive.")

        self.setting = num

    def reset_rotor(self):
        self.set_setting(0)


    def encrypt(self, p):
        """ p is Enter position. 
        Simulates electrical signal arriving and passing through rotor.
        Signal arrives at enter position.
        From Enter position, signal hits input contact. 
        Signal goes through internal mapping and goes to output contact.
        From ouput contact, signal will exit through an exit position.
        Output is output position in numeric form.
        """
        if p < 0 or p > 26:
            raise ValueError("p must between 0 and 26 inclusive.")

        logging.debug("Rotor.encrypt(). Type {}".format(self.type))
        logging.debug("p is {}. alphabetic form is {}".format(p, self.alphabet_map[p]))

        input_contact = (p + self.setting) % 26
        logging.debug("signal hits input_contact {}. alphabetic form is {}".format(input_contact, self.alphabet_map[input_contact]))

        output_contact = self.contact_map[input_contact]
        logging.debug("rotor converts signal to {}. alphabetic form is {}".format(output_contact, self.alphabet_map[output_contact]))

        exit_p = (output_contact - self.setting) % 26
        logging.debug("signal exits at position {}. alphabetic form is {}".format(exit_p, self.alphabet_map[exit_p]))

        return exit_p


    def backwards_encrypt(self, p):
        """ Going from left to right. """
        if p < 0 or p > 26:
            raise ValueError("p must between 0 and 26 inclusive.")

        input_contact = (p + self.setting) % 26
        output_contact = self.contact_map.index(input_contact)    
        exit_p = (output_contact - self.setting) % 26

        # Debug logs
        logging.debug("Rotor.backwards_encrypt(). Type {}".format(self.type))
        logging.debug("signal hits input_contact {}. alphabetic form is {}".format(input_contact, self.alphabet_map[input_contact]))
        logging.debug("rotor converts signal to {}. alphabetic form is {}".format(output_contact, self.alphabet_map[output_contact]))
        logging.debug("signal exits at position {}. alphabetic form is {}".format(exit_p, self.alphabet_map[exit_p]))

        return exit_p


    def __str__(self):
        return "Rotor type {}".format(self.type)

if __name__ == "__main__":
    logging.basicConfig(filename='old_rotor.log', level=logging.DEBUG, filemode='w')
    logging.info('Started')

    # Testing rotor 1

    """ Mapping for Rotor 1:
    0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
    A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z 
    E  K  M  F  L  G  D  Q  V  Z  N  T  O  W  Y  H  X  U  S  P  A  I  B  R  C  J  
    4  10 12 5 ....  
    """
    
    r1_contact_map = [letter for letter in "EKMFLGDQVZNTOWYHXUSPAIBRCJ"]
    rotor_1 = Rotor(1, r1_contact_map, ["Q"]) # If this rotor steps from Q to R, then the next rotor is advanced

    # Test encrypting 'f' with an 'f' setting
    rotor_1.set_setting(5)
    rotor_1.encrypt(5)
    
    # Test reflect encrypt. Apparently works the same left-to-right as it does right-to-left
    print(rotor_1.backwards_encrypt(9))
