import random
import config
from units.piece import PieceType, ChessPiece
from deployment.board_grid import BoardGrid

class AIFormationGenerator:
    def __init__(self, board: BoardGrid):
        self.board = board
        self.ai_pieces = []
        
    def generate_formation(self, current_stage: int):
        # Clear existing AI pieces
        for row in config.AI_DEPLOY_ROWS:
            for col in range(8):
                if self.board.is_occupied(row, col):
                    self.board.remove_piece(row, col)
        self.ai_pieces.clear()
        
        # Pick a random template
        template_name = random.choice(list(config.AI_FORMATIONS.keys()))
        template = config.AI_FORMATIONS[template_name]
        
        print(f"AI using formation: {template_name}")
        budget = config.AI_STAGE_BUDGET_BASE + (current_stage * config.AI_STAGE_BUDGET_MULT)
        
        # Populate back row (Row 0)
        for col, piece_str in enumerate(template["back_row"]):
            if piece_str:
                cost = config.UNIT_DATA[piece_str]["buy_cost"]
                if piece_str == "King" or budget >= cost:
                    piece = ChessPiece(PieceType(piece_str))
                    self.board.place_piece(piece, 0, col)
                    self.ai_pieces.append(piece)
                    budget -= cost
                
        # Populate front row (Row 1)
        for col, piece_str in enumerate(template["front_row"]):
            if piece_str:
                cost = config.UNIT_DATA[piece_str]["buy_cost"]
                # Give a discount to pawn spawns to ensure frontline structure, or strict cost
                if budget >= cost:
                    piece = ChessPiece(PieceType(piece_str))
                    self.board.place_piece(piece, 1, col)
                    self.ai_pieces.append(piece)
                    budget -= cost
