"""
MoneyChess2 Global Configuration
"""

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS_LIMIT = 60

# Economy constants
STARTING_GOLD = 500
SHOP_SIZE = 5
SHOP_REROLL_COST = 10

# Unit Economy & Properties
UNIT_DATA = {
    "Pawn": {
        "buy_cost": 50,
        "sell_value": 25,
        "upkeep": 2,
        "recovery_min": 1,
        "recovery_max": 1,
        "shop_weight": 50
    },
    "Knight": {
        "buy_cost": 150,
        "sell_value": 75,
        "upkeep": 6,
        "recovery_min": 1,
        "recovery_max": 2,
        "shop_weight": 20
    },
    "Bishop": {
        "buy_cost": 150,
        "sell_value": 75,
        "upkeep": 6,
        "recovery_min": 1,
        "recovery_max": 2,
        "shop_weight": 20
    },
    "Rook": {
        "buy_cost": 250,
        "sell_value": 125,
        "upkeep": 10,
        "recovery_min": 2,
        "recovery_max": 3,
        "shop_weight": 10
    },
    "Queen": {
        "buy_cost": 500,
        "sell_value": 250,
        "upkeep": 20,
        "recovery_min": 3,
        "recovery_max": 4,
        "shop_weight": 2
    },
    "King": {
        "buy_cost": 0,
        "sell_value": 0,
        "upkeep": 0,
        "recovery_min": 0,
        "recovery_max": 0,
        "shop_weight": 0
    }
}
