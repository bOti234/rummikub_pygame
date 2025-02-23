from enum import Enum

class COLOURS(Enum):
    NAMES = ["red", "yellow", "black", "blue"]
    RED = 0
    YELLOW = 1
    BLACK = 2
    BLUE = 3
    COLOURS = [RED, YELLOW, BLACK, BLUE]
    
class LOCATIONS(Enum):
    NAMES = ["deck", "hand", "board"]
    DECK = 0
    HAND = 1
    BOARD = 2
    LOCATIONS = [DECK, HAND, BOARD]

class ROWTYPES(Enum):
    NAMES = ["colour", "number"]
    COLOUR = 0
    NUMBER = 1
    ROWTYPES = [COLOUR, NUMBER]

class BUTTONTYPES(Enum):
    NAMES = ["menu", "start", "options", "videosetting", "audiosetting", "exit", "restore", "endturn"]
    MENU = 0
    START = 1
    OPTIONS = 2
    VIDEOSETTING = 3
    AUDIOSETTING = 4
    EXIT = 5
    RESTORE = 6
    ENDTURN = 7
    BUTTONTYPES = [MENU, START, OPTIONS, VIDEOSETTING, AUDIOSETTING, EXIT, RESTORE, ENDTURN]
    INGAME_BUTTONS = [MENU, RESTORE, ENDTURN]
    MENU_BUTTONS = [START, OPTIONS, VIDEOSETTING, AUDIOSETTING, EXIT]

class HOVERED(Enum):
    NAMES = ["none", "left", "right"]
    NONE = 0
    LEFT = 1
    RIGHT = 2
    HOVERED = [NONE, LEFT, RIGHT]