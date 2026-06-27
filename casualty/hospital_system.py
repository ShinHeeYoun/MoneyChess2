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

    def process_enemy_captives(self, captured_ai_units, roster):
        recruits = []
        for piece in captured_ai_units:
            if piece.piece_type.value == "King":
                continue
                
            roll = random.randint(1, 100)
            if roll <= config.CAPTIVE_RECRUIT_CHANCE:
                piece.status = PieceStatus.ACTIVE
                # It inherently switches sides by being added to the player's roster
                roster.add_piece(piece)
                recruits.append(piece)
        return recruits
