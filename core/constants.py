from turtle import Screen

SIZE = 50
W_HEIGHT = 9
W_WIDTH = 14
WINDOW_SIZE = (W_WIDTH * SIZE, W_HEIGHT * SIZE)
myWin = Screen()
ARROWHEAD = 15
SCREEN_COLOR = "white"
GRAPH_AREA = ( (-326, 206), (77, -100) )
GAP = 5
TRUNC = 10 # decimal truncament
EPSILON = 1/(10**(TRUNC-4)) # = 0.000001 because sometime a certain gap must be allowed
POLY_DICT = {"circle" : 72,
             "triangle" : 3,
             "squared" : 4,
             "pentagon": 5,
             "hexagon": 6,
             "heptagon": 7,
             "octagon": 8
             }

BUTTONS_LIST = {}

MESSAGE_TIME = 3
SORTING_TIME_SHORT = 0.5
SORTING_TIME_LONG = 0.7
