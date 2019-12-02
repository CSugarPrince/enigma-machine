import logging

class Reflector():

    def __init__(self, reflector_type, contact_map):

        self.type = reflector_type # UKW-B or UKW-C
        
        # Create contact map for reflector
        self.alphabet_map = [letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        self.contact_map = [letter for letter in contact_map]

    
    def encrypt(self, letter):
        """ No fancy arithmetic since reflectors do not rotate. """
        if letter not in self.alphabet_map:
            raise ValueError("letter must be uppercase alphabetical character.")

        p = self.alphabet_map.index(letter)
        exit_p = self.contact_map[p]
        

        return exit_p


if __name__ == "__main__":

    logging.basicConfig(filename='reflector.log', level=logging.DEBUG, filemode='w')
    logging.info('Started')

    b = Reflector("UKW-B", [letter for letter in "YRUHQSLDPXNGOKMIEBFZCWVJAT"])
    print(b.contact_map)
    
    for x in range(25):
        b.encrypt(x)