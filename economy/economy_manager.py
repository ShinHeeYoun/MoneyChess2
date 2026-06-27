import config
from units.roster import RosterManager

class EconomyManager:
    def __init__(self, starting_gold: int = config.STARTING_GOLD):
        self.current_gold = starting_gold
        self.is_bankrupt = False
        
    def add_gold(self, amount: int):
        if amount > 0:
            self.current_gold += amount
            self.check_bankruptcy_status()
            
    def subtract_gold(self, amount: int) -> bool:
        """Subtracts gold. Returns True if successful, False if insufficient (unless upkeep)."""
        if amount > 0:
            if self.current_gold >= amount:
                self.current_gold -= amount
                return True
            return False
        return True
        
    def calculate_total_upkeep(self, roster: RosterManager) -> int:
        return sum(piece.upkeep for piece in roster.pieces)
        
    def process_upkeep(self, roster: RosterManager):
        total_upkeep = self.calculate_total_upkeep(roster)
        self.current_gold -= total_upkeep
        self.check_bankruptcy_status()
        
    def check_bankruptcy_status(self):
        self.is_bankrupt = self.current_gold < 0
