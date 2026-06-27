import random
import config
from units.piece import PieceType, ChessPiece
from deployment.board_grid import BoardGrid

class AIFormationGenerator:
    def __init__(self, board: BoardGrid):
        self.board = board
        self.ai_pieces = []
        
    def generate_formation_preview(self, current_stage: int, risk_multiplier: float) -> dict:
        budget = (config.AI_STAGE_BUDGET_BASE + (current_stage * config.AI_STAGE_BUDGET_MULT)) * risk_multiplier
        template_name = random.choice(list(config.AI_FORMATIONS.keys()))
        template = config.AI_FORMATIONS[template_name]
        
        preview_counts = {}
        ai_pieces = []
        
        for col, piece_str in enumerate(template["back_row"]):
            if piece_str:
                cost = config.UNIT_DATA[piece_str]["buy_cost"]
                if piece_str == "King" or budget >= cost:
                    ai_pieces.append(PieceType(piece_str))
                    budget -= cost
                    
        for col, piece_str in enumerate(template["front_row"]):
            if piece_str:
                cost = config.UNIT_DATA[piece_str]["buy_cost"]
                if budget >= cost:
                    ai_pieces.append(PieceType(piece_str))
                    budget -= cost
                    
        for pt in ai_pieces:
            preview_counts[pt.value] = preview_counts.get(pt.value, 0) + 1
            
        return {
            "template": template_name,
            "counts": preview_counts,
            "ai_pieces": ai_pieces
        }
        
    def apply_formation(self, formation_preview: dict):
        for row in config.AI_DEPLOY_ROWS:
            for col in range(8):
                if self.board.is_occupied(row, col):
                    self.board.remove_piece(row, col)
        self.ai_pieces.clear()
        
        template = config.AI_FORMATIONS[formation_preview["template"]]
        ai_list = formation_preview["ai_pieces"].copy()
        
        for col, piece_str in enumerate(template["back_row"]):
            if piece_str and PieceType(piece_str) in ai_list:
                piece = ChessPiece(PieceType(piece_str))
                self.board.place_piece(piece, 0, col)
                self.ai_pieces.append(piece)
                ai_list.remove(PieceType(piece_str))
                
        for col, piece_str in enumerate(template["front_row"]):
            if piece_str and PieceType(piece_str) in ai_list:
                piece = ChessPiece(PieceType(piece_str))
                self.board.place_piece(piece, 1, col)
                self.ai_pieces.append(piece)
                ai_list.remove(PieceType(piece_str))
