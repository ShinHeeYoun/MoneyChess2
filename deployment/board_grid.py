import config
from typing import Optional, Tuple
from units.piece import ChessPiece

class BoardGrid:
    def __init__(self):
        # 8x8 grid storing None or ChessPiece
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        
    def screen_to_grid(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        col = (x - config.BOARD_OFFSET_X) // config.GRID_SQUARE_SIZE
        row = (y - config.BOARD_OFFSET_Y) // config.GRID_SQUARE_SIZE
        if 0 <= row < 8 and 0 <= col < 8:
            return (row, col)
        return None
        
    def grid_to_screen(self, row: int, col: int) -> Tuple[int, int]:
        x = config.BOARD_OFFSET_X + (col * config.GRID_SQUARE_SIZE)
        y = config.BOARD_OFFSET_Y + (row * config.GRID_SQUARE_SIZE)
        return (x, y)
        
    def is_occupied(self, row: int, col: int) -> bool:
        if 0 <= row < 8 and 0 <= col < 8:
            return self.grid[row][col] is not None
        return True # Treat out of bounds as occupied
        
    def place_piece(self, piece: ChessPiece, row: int, col: int) -> bool:
        if 0 <= row < 8 and 0 <= col < 8 and not self.is_occupied(row, col):
            self.grid[row][col] = piece
            return True
        return False
        
    def remove_piece(self, row: int, col: int) -> Optional[ChessPiece]:
        if 0 <= row < 8 and 0 <= col < 8:
            piece = self.grid[row][col]
            self.grid[row][col] = None
            return piece
        return None
