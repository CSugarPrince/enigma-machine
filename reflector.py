import logging

class Reflector():

    def __init__(self, reflector_type, contact_map):

        self.type = reflector_type # UKW-B or UKW-C
        
        # Create contact map for reflector
        self.alphabet_map = [letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        self.contact_map = [self.alphabet_map.index(let) for let in contact_map]

    
    def encrypt(self, p):
        """ No fancy arithmetic since reflectors do not rotate. """

        if p < 0 or p > 26:
            raise ValueError("p must between 0 and 26 inclusive.")

        logging.debug("Reflector.encrypt(). Type {}".format(self.type))
        logging.debug("p is {}. alphabetic form is {}".format(p, self.alphabet_map[p]))

        exit_p = self.contact_map[p]
        logging.debug("signal exits at position {}. alphabetic form is {}".format(exit_p, self.alphabet_map[exit_p]))

        return exit_p


if __name__ == "__main__":

    logging.basicConfig(filename='reflector.log', level=logging.DEBUG, filemode='w')
    logging.info('Started')

    b = Reflector("UKW-B", [letter for letter in "YRUHQSLDPXNGOKMIEBFZCWVJAT"])
    print(b.contact_map)
    
    for x in range(25):
        b.encrypt(x)