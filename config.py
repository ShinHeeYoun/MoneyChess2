"""
MoneyChess2 Global Configuration
"""
import os
import pygame

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS_LIMIT = 60

# Asset Directory
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "pieces")

# Persistence settings
SAVE_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save_game.json")

# Button UI configurations
BUTTON_COLOR_NEUTRAL = (30, 32, 34)
BUTTON_COLOR_HOVER = (50, 52, 54)
BUTTON_TEXT_COLOR = (240, 240, 240)

# Modern Tactical Colors
BACKGROUND_COLOR = (24, 26, 27)
PANEL_COLOR = (18, 19, 20)
PANEL_BORDER_COLOR = (80, 80, 80)
ACCENT_COLOR = (218, 165, 32)
TEXT_COLOR = (240, 240, 240)

# Chess.com Palette
COLOR_SQUARE_LIGHT = (238, 238, 212)
COLOR_SQUARE_DARK = (118, 150, 86)

# Layout Bounding Boxes
LEFT_PANEL_RECT = pygame.Rect(0, 0, 300, WINDOW_HEIGHT)
RIGHT_PANEL_RECT = pygame.Rect(WINDOW_WIDTH - 300, 0, 300, WINDOW_HEIGHT)
CENTER_BOARD_RECT = pygame.Rect(300, 0, WINDOW_WIDTH - 600, WINDOW_HEIGHT)

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
MATERIAL_VALUES = {"Pawn": 10, "Knight": 30, "Bishop": 30, "Rook": 50, "Queen": 90, "King": 0}

# Captive System
CAPTIVE_RECRUIT_CHANCE = 10

# Victory Condition
VICTORY_CONDITION = "ELIMINATE_KING"

# Board Configurations
GRID_SQUARE_SIZE = 80
BOARD_OFFSET_X = CENTER_BOARD_RECT.x + (CENTER_BOARD_RECT.width - (8 * GRID_SQUARE_SIZE)) // 2
BOARD_OFFSET_Y = CENTER_BOARD_RECT.y + (CENTER_BOARD_RECT.height - (8 * GRID_SQUARE_SIZE)) // 2

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
        "buy_cost": 10,
        "sell_value": 5,
        "upkeep": 0,
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
