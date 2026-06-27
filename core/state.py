from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    MANAGEMENT = auto()
    STAGE_SELECT = auto()
    DEPLOYMENT = auto()
    COMBAT = auto()
    RESOLUTION = auto()
    GAME_OVER = auto()
