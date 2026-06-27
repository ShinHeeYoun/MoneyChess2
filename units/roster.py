from typing import List, Optional
from units.piece import ChessPiece, PieceStatus
import uuid

class RosterManager:
    def __init__(self):
        self.pieces: List[ChessPiece] = []
        
    def add_piece(self, piece: ChessPiece):
        self.pieces.append(piece)
        
    def remove_piece(self, piece_id: uuid.UUID) -> bool:
        for piece in self.pieces:
            if piece.id == piece_id:
                self.pieces.remove(piece)
                return True
        return False
        
    def get_piece(self, piece_id: uuid.UUID) -> Optional[ChessPiece]:
        for piece in self.pieces:
            if piece.id == piece_id:
                return piece
        return None
        
    def get_active_units(self) -> List[ChessPiece]:
        return [p for p in self.pieces if p.status == PieceStatus.ACTIVE]
        
    def get_injured_units(self) -> List[ChessPiece]:
        return [p for p in self.pieces if p.status == PieceStatus.INJURED]
        
    def tick_hospital_turns(self):
        for piece in self.pieces:
            if piece.status == PieceStatus.INJURED:
                if piece.current_injury_turns > 0:
                    piece.current_injury_turns -= 1
                if piece.current_injury_turns <= 0:
                    piece.status = PieceStatus.ACTIVE
