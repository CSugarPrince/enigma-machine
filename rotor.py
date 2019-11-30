from copy import deepcopy

class Rotor():

    def __init__(self, name, wiring_map, notches):

        # Alphabet map
        self.a = [letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

        self.name = name # I, II, III, etc...
        self.ringstellung = "A"
        self.rotation_offset = "A" 
        self.notches = notches

        # Create representation of internal wiring / rotor's inner core
        self.right = [letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        self.left = [None for x in range(26)]
        

        # Create left from map
        for letter in wiring_map:
            i = wiring_map.index(letter) # 0
            let = self.a[i] # A
            j = self.let_to_num(letter) # 4
            self.left[j] = let

        
        # Save initial settings for rotor
        self.right_initial = deepcopy(self.right)
        self.left_initial = deepcopy(self.left)

        # Print rotor internals
        #self.print_internals()

    
    def print_internals(self):
        print(self.name, "ring setting:", self.ringstellung,"rotation_offset:", self.rotation_offset)
        for letter in self.a:
            i = self.a.index(letter)
            print(letter, self.left[i], self.right[i], letter)

    def let_to_num(self, letter):
        alphabet = [let for let in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        if letter not in alphabet:
            raise ValueError("letter must be alphabetical and uppercase. e.g. 'A'")

        return alphabet.index(letter)

    def rotate(self):
        i = self.a.index(self.rotation_offset)
        j = (i+1) % 26
        self.rotation_offset = self.a[j]

        # Rotate rotor's inner core up / left by one
        self.right = self.right[1:] + self.right[:1]
        self.left = self.left[1:] + self.left[:1]

         
    def set_ringstellung(self, letter):
        self.reset()

        # Rotate inner core down / right
        num = self.a.index(letter)
        self.right = self.right[-num:] + self.right[:-num]
        self.left = self.left[-num:] + self.left[:-num]

        self.ringstellung = letter


    def reset(self):
        self.ringstellung = "A"
        self.rotation_offset = "A" # Being safe

        self.right = deepcopy(self.right_initial)
        self.left = deepcopy(self.left_initial)

    
    def encrypt(self, let):
        if let not in self.a:
            raise ValueError("letter must be uppercase alphabetical character.")

        # Ex: encrypt 'A'. Rotor I. Ring setting 'B'. Offset 'A'
        i = self.a.index(let) # 0
        
        r = self.right[i] # Z

        j = self.left.index(r) # 10

        out = self.a[j] # K

        return out


    def backwards_encrypt(self, let):
        if let not in self.a:
            raise ValueError("letter must be uppercase alphabetical character.")

        # Ex: encrypt 'C'. Rotor I. Ring setting 'A'. Offset 'C'
        i = self.a.index(let) # 2

        l = self.left[i] # A

        j = self.right.index(l) # 24

        out = self.a[j] # Y

        return out


    def set_initial_offset(self, let):
        if let not in self.a:
            raise ValueError("let has to be uppercase alphabetic character.")
        
        # Rotor could be out of inital offset position.
        while self.rotation_offset != let:
            self.rotate()
        

if __name__ == "__main__":
    # Create rotor I
    I = Rotor("I.", [letter for letter in "EKMFLGDQVZNTOWYHXUSPAIBRCJ"], ["Q"])

    # General rotor method tests:
    # Test rotating 27 times
    for i in range(27):
        I.rotate()
        #I.print_internals() Good

    # Test set_ringstellung. all letters in alphabet.
    for letter in I.a:
        I.set_ringstellung(letter)
        I.print_internals()

    # Encrypt alphabet. ringstellung 'A'. offset 'A'
    print("# Encrypt alphabet. ringstellung 'A'. offset 'A'")
    I.set_ringstellung('A')
    out = []
    for x in I.a:
        cipher = I.encrypt(x)
        out.append(cipher)

    ans = [x for x in "EKMFLGDQVZNTOWYHXUSPAIBRCJ"]
    print(out)
    print(ans)

    # Encrypt alphabet. ringstellung 'B'. offset 'A'
    print("# Encrypt alphabet. ringstellung 'B'. offset 'A'")
    I.set_ringstellung('B')
    out = []
    for x in I.a:
        cipher = I.encrypt(x)
        out.append(cipher)

    ans = [x for x in "KFLNGMHERWAOUPXZIYVTQBJCSD"]
    print(out)
    print(ans)



    # Set initial_rotational_offset 'C'
    print("# Set initial_rotational_offset 'C'")
    I.set_initial_offset('C')
    I.print_internals()

    # Set initial_rotational_offset 'B'
    print("# Set initial_rotational_offset 'B'")
    I.set_initial_offset('B')
    I.print_internals()