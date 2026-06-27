from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    MANAGEMENT = auto()
    DEPLOYMENT = auto()
    COMBAT = auto()
    RESOLUTION = auto()
    GAME_OVER = auto()
