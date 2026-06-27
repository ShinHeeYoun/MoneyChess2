import random
import config
from typing import Optional, Tuple
from deployment.board_grid import BoardGrid
from units.piece import PieceType
from combat.move_validation import get_valid_moves
from combat.capture_events import CaptureBuffer
from deployment.deployment_manager import DeploymentManager
from deployment.ai_formations import AIFormationGenerator

class CombatEngine:
    def __init__(self, board: BoardGrid, deployment_mgr: DeploymentManager, ai_gen: AIFormationGenerator):
        self.board = board
        self.deployment_mgr = deployment_mgr
        self.ai_gen = ai_gen
        
        self.capture_buffer = CaptureBuffer()
        
        self.is_player_turn = True
        self.selected_pos: Optional[Tuple[int, int]] = None
        self.valid_moves = []
        
        self.outcome = None # "VICTORY" or "DEFEAT"
        
    def start_combat(self):
        self.capture_buffer.clear()
        self.is_player_turn = True
        self.selected_pos = None
        self.valid_moves = []
        self.outcome = None
        
    def is_player_piece(self, piece):
        return piece.id in self.deployment_mgr.placed_pieces
        
    def is_ai_piece(self, piece):
        return piece in self.ai_gen.ai_pieces
        
    def get_player_pieces_list(self):
        player_pieces = [self.deployment_mgr.roster.get_piece(pid) for pid in self.deployment_mgr.placed_pieces.keys()]
        return [p for p in player_pieces if p is not None]
        
    def get_ai_pieces_list(self):
        return self.ai_gen.ai_pieces
        
    def check_victory_condition(self):
        player_pieces = self.get_player_pieces_list()
        ai_pieces = self.get_ai_pieces_list()
        
        if config.VICTORY_CONDITION == "ELIMINATE_KING":
            player_king_dead = not any(p.piece_type == PieceType.KING for p in player_pieces)
            ai_king_dead = not any(p.piece_type == PieceType.KING for p in ai_pieces)
            if player_king_dead:
                return "DEFEAT"
            if ai_king_dead:
                return "VICTORY"
        else:
            if not player_pieces:
                return "DEFEAT"
            if not ai_pieces:
                return "VICTORY"
        return None
        
    def handle_click(self, row: int, col: int):
        if not self.is_player_turn or self.outcome:
            return
            
        piece = self.board.grid[row][col]
        
        if self.selected_pos:
            if (row, col) in self.valid_moves:
                self.execute_move(self.selected_pos, (row, col))
                self.selected_pos = None
                self.valid_moves = []
                self.check_end_turn()
            else:
                if piece and self.is_player_piece(piece):
                    self.selected_pos = (row, col)
                    self.valid_moves = get_valid_moves(self.board, row, col, True, self.get_player_pieces_list(), self.get_ai_pieces_list())
                else:
                    self.selected_pos = None
                    self.valid_moves = []
        else:
            if piece and self.is_player_piece(piece):
                self.selected_pos = (row, col)
                self.valid_moves = get_valid_moves(self.board, row, col, True, self.get_player_pieces_list(), self.get_ai_pieces_list())
                
    def execute_move(self, start_pos, target_pos):
        start_row, start_col = start_pos
        target_row, target_col = target_pos
        
        moving_piece = self.board.grid[start_row][start_col]
        target_piece = self.board.grid[target_row][target_col]
        
        if target_piece:
            if self.is_player_piece(target_piece):
                self.capture_buffer.add_player_capture(target_piece)
                del self.deployment_mgr.placed_pieces[target_piece.id]
            else:
                self.capture_buffer.add_ai_capture(target_piece)
                self.ai_gen.ai_pieces.remove(target_piece)
                
        # Move on grid
        self.board.grid[target_row][target_col] = moving_piece
        self.board.grid[start_row][start_col] = None
        
        # Update deployment tracker if it's a player piece
        if self.is_player_piece(moving_piece):
            self.deployment_mgr.placed_pieces[moving_piece.id] = (target_row, target_col)
            
    def check_end_turn(self):
        self.outcome = self.check_victory_condition()
        if not self.outcome:
            self.is_player_turn = not self.is_player_turn
            
    def execute_ai_turn(self):
        if self.is_player_turn or self.outcome:
            return
            
        all_moves = []
        ai_pieces_list = self.get_ai_pieces_list()
        player_pieces_list = self.get_player_pieces_list()
        
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece in ai_pieces_list:
                    moves = get_valid_moves(self.board, row, col, False, player_pieces_list, ai_pieces_list)
                    for r, c in moves:
                        target = self.board.grid[r][c]
                        is_capture = target is not None and self.is_player_piece(target)
                        all_moves.append({
                            'start': (row, col),
                            'target': (r, c),
                            'is_capture': is_capture
                        })
                        
        if all_moves:
            # Prioritize captures
            captures = [m for m in all_moves if m['is_capture']]
            if captures:
                move = random.choice(captures)
            else:
                move = random.choice(all_moves)
                
            self.execute_move(move['start'], move['target'])
            
        self.check_end_turn()
