import random
import config
from units.piece import PieceStatus

class CasualtyProcessor:
    def process_casualties(self, captured_units, roster):
        results = []
        for piece in captured_units:
            matrix = config.CASUALTY_PROBABILITY_MATRIX[piece.piece_type.value]
            roll = random.randint(1, 100)
            
            if roll <= matrix["HEALTHY"]:
                outcome = "HEALTHY"
                piece.status = PieceStatus.ACTIVE
            elif roll <= matrix["HEALTHY"] + matrix["INJURED"]:
                outcome = "INJURED"
                piece.roll_injury_turns()
            else:
                outcome = "DEAD"
                piece.status = PieceStatus.DEAD
                roster.remove_piece(piece.id)
                
            results.append((piece, outcome))
        return results
