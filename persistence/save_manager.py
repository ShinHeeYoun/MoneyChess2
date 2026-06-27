import json
import os
import uuid
import config
from units.piece import ChessPiece, PieceType, PieceStatus
from units.roster import RosterManager
from economy.economy_manager import EconomyManager

class SaveManager:
    @staticmethod
    def save_game(economy_manager: EconomyManager, roster_manager: RosterManager, current_stage: int):
        data = {
            "current_stage": current_stage,
            "current_gold": economy_manager.current_gold,
            "pieces": []
        }
        
        for piece in roster_manager.pieces:
            data["pieces"].append({
                "id": str(piece.id),
                "piece_type": piece.piece_type.value,
                "status": piece.status.name,
                "current_injury_turns": piece.current_injury_turns
            })
            
        with open(config.SAVE_FILE_PATH, 'w') as f:
            json.dump(data, f, indent=4)
            
    @staticmethod
    def load_game(economy_manager: EconomyManager, roster_manager: RosterManager) -> int:
        if not os.path.exists(config.SAVE_FILE_PATH):
            return 1
            
        with open(config.SAVE_FILE_PATH, 'r') as f:
            data = json.load(f)
            
        economy_manager.current_gold = data.get("current_gold", config.STARTING_GOLD)
        current_stage = data.get("current_stage", 1)
        
        roster_manager.pieces.clear()
        for p_data in data.get("pieces", []):
            piece = ChessPiece(PieceType(p_data["piece_type"]))
            piece.id = uuid.UUID(p_data["id"])
            piece.status = PieceStatus[p_data["status"]]
            piece.current_injury_turns = p_data.get("current_injury_turns", 0)
            roster_manager.add_piece(piece)
            
        return current_stage
