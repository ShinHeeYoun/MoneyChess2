import pygame
import config
from typing import Optional
from units.piece import ChessPiece
from units.roster import RosterManager
from deployment.board_grid import BoardGrid

class DeploymentManager:
    def __init__(self, board: BoardGrid, roster: RosterManager):
        self.board = board
        self.roster = roster
        self.dragging_piece: Optional[ChessPiece] = None
        
        # Track pieces that have been placed on the board by the player
        # Maps piece.id to (row, col)
        self.placed_pieces = {}
        
    def get_unplaced_active_units(self):
        active_units = self.roster.get_active_units()
        return [p for p in active_units if p.id not in self.placed_pieces]
        
    def handle_mouse_down(self, pos: tuple):
        x, y = pos
        # Check if clicking on an already placed piece to move it
        grid_pos = self.board.screen_to_grid(x, y)
        if grid_pos:
            row, col = grid_pos
            if row in config.PLAYER_DEPLOY_ROWS and self.board.is_occupied(row, col):
                piece = self.board.grid[row][col]
                # Make sure it's a player piece (id in roster)
                if self.roster.get_piece(piece.id):
                    self.dragging_piece = self.board.remove_piece(row, col)
                    if self.dragging_piece.id in self.placed_pieces:
                        del self.placed_pieces[self.dragging_piece.id]
                    return
                    
        # Check if clicking on the unplaced roster sidebar
        unplaced = self.get_unplaced_active_units()
        sidebar_x = 20
        sidebar_y_start = 200
        for i, piece in enumerate(unplaced):
            rect = pygame.Rect(sidebar_x, sidebar_y_start + i * 40, 150, 30)
            if rect.collidepoint(x, y):
                self.dragging_piece = piece
                return
                
    def handle_mouse_up(self, pos: tuple):
        if self.dragging_piece:
            x, y = pos
            grid_pos = self.board.screen_to_grid(x, y)
            
            if grid_pos:
                row, col = grid_pos
                # Validate player drop zone
                if row in config.PLAYER_DEPLOY_ROWS and not self.board.is_occupied(row, col):
                    self.board.place_piece(self.dragging_piece, row, col)
                    self.placed_pieces[self.dragging_piece.id] = (row, col)
            self.dragging_piece = None
            
    def clear_deployment(self):
        for row in config.PLAYER_DEPLOY_ROWS:
            for col in range(8):
                if self.board.is_occupied(row, col):
                    piece = self.board.grid[row][col]
                    if self.roster.get_piece(piece.id):
                        self.board.remove_piece(row, col)
        self.placed_pieces.clear()
