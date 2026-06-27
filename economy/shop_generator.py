import random
import config
from typing import List
from units.piece import PieceType, ChessPiece
from units.roster import RosterManager
from economy.economy_manager import EconomyManager
import uuid

class ShopManager:
    def __init__(self, economy_manager: EconomyManager, roster_manager: RosterManager):
        self.economy = economy_manager
        self.roster = roster_manager
        self.current_shop: List[PieceType] = []
        
        # Prepare weighted pool for pieces
        self.piece_pool = []
        self.piece_weights = []
        for piece_name, data in config.UNIT_DATA.items():
            if data["shop_weight"] > 0:
                self.piece_pool.append(PieceType(piece_name))
                self.piece_weights.append(data["shop_weight"])
                
    def generate_shop(self):
        self.current_shop = random.choices(
            population=self.piece_pool,
            weights=self.piece_weights,
            k=config.SHOP_SIZE
        )
        
    def reroll_shop(self) -> bool:
        if self.economy.is_bankrupt:
            return False
            
        if self.economy.subtract_gold(config.SHOP_REROLL_COST):
            self.generate_shop()
            return True
        return False
        
    def buy_piece(self, index: int) -> bool:
        if self.economy.is_bankrupt:
            return False
            
        if 0 <= index < len(self.current_shop):
            piece_type = self.current_shop[index]
            cost = config.UNIT_DATA[piece_type.value]["buy_cost"]
            
            if self.economy.subtract_gold(cost):
                new_piece = ChessPiece(piece_type)
                self.roster.add_piece(new_piece)
                # Remove from shop after purchase
                self.current_shop.pop(index)
                return True
        return False
        
    def sell_piece(self, piece_id: uuid.UUID) -> bool:
        piece = self.roster.get_piece(piece_id)
        if piece:
            if piece.piece_type == PieceType.KING or str(piece.piece_type.value).upper() == "KING":
                print("WARNING: You cannot sell the King!")
                return False
                
            self.economy.add_gold(piece.sell_value)
            self.roster.remove_piece(piece_id)
            return True
        return False
