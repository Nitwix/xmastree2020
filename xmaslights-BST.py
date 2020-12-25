# yes, it's bad to hardcode this way, but this way it doesn't change
# the code structure too much x)
PIXEL_COUNT = 500

def valueToGRB(value):
    """
    Converts a 32 bit int to its GRB components
    """
    assert Node.MIN_VALUE <= value and value < Node.MAX_VALUE
    B = value & 0xFF
    R = (value & 0xFF00) >> 8
    G = (value & 0xFF0000) >> 16
    return [G, R, B]

class Node:
    """
    This class represents a node of the BST
    """
    MIN_VALUE = 255 # so its never 100% dark
    MAX_VALUE = 1 << 24 # three 8-bit values
    pixels = None
    sorted_coords_w_idx = None # [x,y,z,led_idx]
    def __init__(self, idx, value):
        """
        idx is index of the node in the BST. This is useful to retreive the 
            led index (see get_led_idx)
        value is the value stored in the node. This then determines the color of
            the corresponding led
        """
        # initialisation must be done before making a node
        assert 0 <= idx # and led_idx < 500, but don't want to hardcode 500
        assert Node.MIN_VALUE <= value and value < Node.MAX_VALUE
        self.lchild = None
        self.rchild = None
        self.idx = idx # index of the led in pixels
        self.value = value
    
    def lchild_idx(self):
        """
        returns the index of the left child. 
        This way, because my list is sorted by height, the children will be
        physically below their parents. 
        """
        return 2*self.idx + 1
    def rchild_idx(self):
        """
        returns the index of the right child. 
        """
        return 2*self.idx + 2

    def get_led_idx(self):
        """
        Gets the index of the corresponding led in the pixels array
        """
        return Node.sorted_coords_w_idx[self.idx][3]

    def insert_rnd_val(self):
        """
        Insert new random value into the tree
        Returns whether the insertion was successful (True) or not (False)
        """
        import random
        rnd_val = random.randrange(Node.MIN_VALUE, Node.MAX_VALUE)
        return self.insert(rnd_val)



    def blink_led(self, value):
        """
        Blink the corresponding led with value as color.
        This is used to "show" the path that a new insertion takes.
        Each time a new value passes through some intermediate node,
        it makes it blink to show that it went through there.
        """
        import time
        # TODO change back to .5
        blink_delay = 0.1
        led_idx = self.get_led_idx()
        GRB = valueToGRB(value)
        print("blink:", GRB, " at ", led_idx)
        # TODO RE-ENABLE!!!
        # old_GRB = pixels[led_idx]
        # pixels[led_idx] = [0,0,0]
        # pixels.show()
        # time.sleep(blink_delay)
        # pixels[led_idx] = GRB
        # pixels.show()
        # time.sleep(blink_delay)
        # pixels[led_idx] = old_GRB
        # pixels.show()

        print("[0,0,0]")
        time.sleep(blink_delay)
        print(GRB)
        time.sleep(blink_delay)
        print("old GRB")


    def show_led(self):
        """
        Shows the led corresponding to this node
        """
        GRB = valueToGRB(self.value)
        # TODO RE-ENABLE!!!
        # pixels[self.get_led_idx()] = GRB
        # pixels.show()
        print("set led to", GRB)

    def insert(self, value):
        """
        Inserts the given value from the current node (self)
        It will recursively insert until it finds a spot that is empty
        """
        if value < self.value:
            if self.lchild_idx() >= PIXEL_COUNT:
                return False 
            if self.lchild == None:
                self.lchild = Node(self.lchild_idx(), value)
                self.lchild.show_led()
                print("Inserted ", value, " at index ", self.lchild.get_led_idx(), '\n')
            else:
                self.blink_led(value)
                return self.lchild.insert(value)
        else:
            if self.rchild_idx() >= PIXEL_COUNT:
                return False
            if self.rchild == None:
                self.rchild = Node(self.rchild_idx(), value)
                self.rchild.show_led()
                print("Inserted ", value, " at index ", self.rchild.get_led_idx(), '\n')
            else:
                self.blink_led(value)
                return self.rchild.insert(value)
        return True # insertion succesful

def clear_pixels(pixels):
    """
    Clears the pixels array and calls show()
    This is useful at the end of the construction of a BST
    to clear for the next BST.
    """
    for led_idx in range(PIXEL_COUNT):
        pixels[led_idx] = [0,0,0]
    # TODO RE-ENABLE!!!
    # pixels.show()
    print('\n' , "Cleared pixels", '\n')


def xmaslight():
    # This is the code from my 
    
    #NOTE THE LEDS ARE GRB COLOUR (NOT RGB)
    
    # Here are the libraries I am currently using:
    import time
    # TODO RE-ENABLE !!!
    # import board
    # import neopixel
    import re
    import math
    
    # You are welcome to add any of these:
    # import random
    import numpy as np
    # import scipy
    # import sys
    
    # If you want to have user changable values, they need to be entered from the command line
    # so import sys sys and use sys.argv[0] etc
    # some_value = int(sys.argv[0])
    
    # IMPORT THE COORDINATES (please don't break this bit)
    
    # TODO RE-ENABLE!!!
    # coordfilename = "Python/coords.txt"
    coordfilename = "coords.txt"
	
    fin = open(coordfilename,'r')
    coords_raw = fin.readlines()
    
    coords_bits = [i.split(",") for i in coords_raw]
    
    coords = []
    
    for slab in coords_bits:
        new_coord = []
        for i in slab:
            new_coord.append(int(re.sub(r'[^-\d]','', i)))
        coords.append(new_coord)
    
    #set up the pixels (AKA 'LEDs')
    PIXEL_COUNT = len(coords) # this should be 500
    
    # TODO RE-ENABLE!!!
    # pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, auto_write=False)
    
    
    # YOU CAN EDIT FROM HERE DOWN
    # add index to keep track of the led index
    coords_w_idx = []
    for i, coord in enumerate(coords):
        x,y,z = coord
        coords_w_idx.append([x,y,z,i])
    coords_np = np.array(coords_w_idx)

    #first we sort the coordinates by height (in increasing order)
    sorted_incr = coords_np[coords_np[:,2].argsort()]
    # now flip to have by decreasing height
    sorted = np.flip(sorted_incr, axis=0)
    print(sorted[:10, :])

    # TODO RE-ENABLE!!!
    Node.pixels = [] #pixels
    Node.sorted_coords_w_idx = sorted
    root = Node(idx=0, value=int(Node.MAX_VALUE/2))
    root.show_led()

    # print(root)
    while True:
        could_insert = True
        while could_insert:
            could_insert = root.insert_rnd_val()
        # TODO RE-ENABLE!!!
        #clear_pixels(pixels)
        clear_pixels(np.zeros((PIXEL_COUNT, 3)))
        # make a new root
        root = Node(idx=0, value=int(Node.MAX_VALUE/2))
        root.show_led()
    return 'DONE'


# yes, I just put this at the bottom so it auto runs
xmaslight()
