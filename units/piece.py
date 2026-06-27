import uuid
from enum import Enum, auto
import config
import random

class PieceType(Enum):
    PAWN = "Pawn"
    KNIGHT = "Knight"
    BISHOP = "Bishop"
    ROOK = "Rook"
    QUEEN = "Queen"
    KING = "King"

class PieceStatus(Enum):
    ACTIVE = auto()
    INJURED = auto()
    DEAD = auto()

class ChessPiece:
    def __init__(self, piece_type: PieceType):
        self.id = uuid.uuid4()
        self.piece_type = piece_type
        self.status = PieceStatus.ACTIVE
        self.current_injury_turns = 0
        
        data = config.UNIT_DATA[self.piece_type.value]
        self.buy_cost = data["buy_cost"]
        self.sell_value = data["sell_value"]
        self.upkeep = data["upkeep"]
        
    def roll_injury_turns(self):
        data = config.UNIT_DATA[self.piece_type.value]
        self.current_injury_turns = random.randint(data["recovery_min"], data["recovery_max"])
        self.status = PieceStatus.INJURED
