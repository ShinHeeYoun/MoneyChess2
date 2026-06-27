"""
MoneyChess2 Global Configuration
"""
import os

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS_LIMIT = 60

# Asset Directory
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "pieces")

# Persistence settings
SAVE_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save_game.json")

# Button UI configurations
BUTTON_COLOR_NEUTRAL = (70, 70, 70)
BUTTON_COLOR_HOVER = (100, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Progression settings
AI_STAGE_BUDGET_BASE = 100
AI_STAGE_BUDGET_MULT = 50

# Contract Selection parameters
CONTRACTS = {
    "Low": {"budget_mult": 0.8, "reward_mult": 0.8, "name": "Low Risk"},
    "Medium": {"budget_mult": 1.0, "reward_mult": 1.0, "name": "Medium Risk"},
    "High": {"budget_mult": 1.5, "reward_mult": 1.5, "name": "High Risk"}
}

# Economy constants
STARTING_GOLD = 500
SHOP_SIZE = 5
SHOP_REROLL_COST = 10

# Combat Rewards
BASE_VICTORY_REWARD = 200
DEFEAT_REWARD = 50

# Victory Condition
VICTORY_CONDITION = "ELIMINATE_KING"

# Board Configurations
GRID_SQUARE_SIZE = 80
BOARD_OFFSET_X = (WINDOW_WIDTH - (8 * GRID_SQUARE_SIZE)) // 2
BOARD_OFFSET_Y = (WINDOW_HEIGHT - (8 * GRID_SQUARE_SIZE)) // 2

# Deployment Zones
PLAYER_DEPLOY_ROWS = [6, 7]
AI_DEPLOY_ROWS = [0, 1]

# AI Formation Templates
AI_FORMATIONS = {
    "Vanguard": {
        "front_row": ["Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn"],
        "back_row": [None, "Knight", "Knight", "Queen", "King", "Knight", "Knight", None]
    },
    "Defensive": {
        "front_row": [None, "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", None],
        "back_row": ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]
    },
    "Standard": {
        "front_row": ["Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn"],
        "back_row": ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]
    }
}

# Unit Economy & Properties
UNIT_DATA = {
    "Pawn": {
        "buy_cost": 50,
        "sell_value": 25,
        "upkeep": 1,
        "recovery_min": 1,
        "recovery_max": 1,
        "shop_weight": 0
    },
    "Knight": {
        "buy_cost": 150,
        "sell_value": 75,
        "upkeep": 3,
        "recovery_min": 1,
        "recovery_max": 2,
        "shop_weight": 20
    },
    "Bishop": {
        "buy_cost": 150,
        "sell_value": 75,
        "upkeep": 3,
        "recovery_min": 1,
        "recovery_max": 2,
        "shop_weight": 20
    },
    "Rook": {
        "buy_cost": 250,
        "sell_value": 125,
        "upkeep": 5,
        "recovery_min": 2,
        "recovery_max": 3,
        "shop_weight": 10
    },
    "Queen": {
        "buy_cost": 500,
        "sell_value": 250,
        "upkeep": 9,
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

CASUALTY_PROBABILITY_MATRIX = {
    "Pawn": {"HEALTHY": 60, "INJURED": 30, "DEAD": 10},
    "Knight": {"HEALTHY": 50, "INJURED": 40, "DEAD": 10},
    "Bishop": {"HEALTHY": 50, "INJURED": 40, "DEAD": 10},
    "Rook": {"HEALTHY": 40, "INJURED": 40, "DEAD": 20},
    "Queen": {"HEALTHY": 30, "INJURED": 50, "DEAD": 20},
    "King": {"HEALTHY": 100, "INJURED": 0, "DEAD": 0}
}
