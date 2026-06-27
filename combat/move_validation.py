from typing import List, Tuple
from deployment.board_grid import BoardGrid
from units.piece import PieceType

def get_valid_moves(board: BoardGrid, start_row: int, start_col: int, is_player: bool, player_pieces: list, ai_pieces: list) -> List[Tuple[int, int]]:
    piece = board.grid[start_row][start_col]
    if not piece:
        return []
        
    valid_moves = []
    
    def is_enemy(r, c):
        target = board.grid[r][c]
        if not target:
            return False
            
        enemy_list = ai_pieces if is_player else player_pieces
        
        if target in enemy_list:
            if target.piece_type == PieceType.KING:
                nobles = [PieceType.KNIGHT, PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN]
                for p in enemy_list:
                    if p.piece_type in nobles:
                        return False # Royal Guard active: King is treated as an impassable/non-targetable obstacle
            return True
        return False
            
    def is_empty(r, c):
        return not board.is_occupied(r, c)
        
    def add_ray(row_dir, col_dir):
        r, c = start_row + row_dir, start_col + col_dir
        while 0 <= r < 8 and 0 <= c < 8:
            if is_empty(r, c):
                valid_moves.append((r, c))
            elif is_enemy(r, c):
                valid_moves.append((r, c))
                break
            else:
                break
            r += row_dir
            c += col_dir

    if piece.piece_type == PieceType.PAWN:
        direction = -1 if is_player else 1
        start_r = 6 if is_player else 1
        
        # Forward 1
        fwd_r = start_row + direction
        if 0 <= fwd_r < 8 and is_empty(fwd_r, start_col):
            valid_moves.append((fwd_r, start_col))
            # Forward 2 from start
            if start_row == start_r:
                fwd2_r = start_row + 2 * direction
                if is_empty(fwd2_r, start_col):
                    valid_moves.append((fwd2_r, start_col))
                    
        # Captures
        for dc in [-1, 1]:
            cap_r, cap_c = start_row + direction, start_col + dc
            if 0 <= cap_r < 8 and 0 <= cap_c < 8 and is_enemy(cap_r, cap_c):
                valid_moves.append((cap_r, cap_c))
                
    elif piece.piece_type == PieceType.KNIGHT:
        knight_moves = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
        for dr, dc in knight_moves:
            r, c = start_row + dr, start_col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if is_empty(r, c) or is_enemy(r, c):
                    valid_moves.append((r, c))
                    
    elif piece.piece_type == PieceType.BISHOP:
        for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            add_ray(dr, dc)
            
    elif piece.piece_type == PieceType.ROOK:
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            add_ray(dr, dc)
            
    elif piece.piece_type == PieceType.QUEEN:
        for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0), (0,-1), (0,1)]:
            add_ray(dr, dc)
            
    elif piece.piece_type == PieceType.KING:
        king_moves = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for dr, dc in king_moves:
            r, c = start_row + dr, start_col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if is_empty(r, c) or is_enemy(r, c):
                    valid_moves.append((r, c))

    return valid_moves
