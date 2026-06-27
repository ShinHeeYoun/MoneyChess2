"""
MoneyChess2 Global Configuration
"""

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS_LIMIT = 60

# Economy constants
STARTING_GOLD = 100
SHOP_REROLL_COST = 5
BANKRUPTCY_THRESHOLD = 0
BANKRUPTCY_PENALTY_MORALE = 10 

# Unit Economy
UNIT_BASE_COST = {
    "Pawn": 10,
    "Knight": 30,
    "Bishop": 30,
    "Rook": 50,
    "Queen": 90,
    "King": 0
}

UNIT_UPKEEP = {
    "Pawn": 1,
    "Knight": 3,
    "Bishop": 3,
    "Rook": 5,
    "Queen": 10,
    "King": 0
}

UNIT_SELL_MARGIN = 0.5 

# Hospital Recovery Parameters
HOSPITAL_RECOVERY_TURNS = {
    "Pawn": {"min": 1, "max": 1},
    "Knight": {"min": 1, "max": 2},
    "Bishop": {"min": 1, "max": 2},
    "Rook": {"min": 2, "max": 3},
    "Queen": {"min": 3, "max": 4},
    "King": {"min": 0, "max": 0}
}
