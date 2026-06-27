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
        self.drag_source_pos = None
        
    def get_unplaced_active_units(self):
        active_units = self.roster.get_active_units()
        return [p for p in active_units if p.id not in self.placed_pieces]
        
    def auto_deploy(self):
        unplaced = self.get_unplaced_active_units()
        if not unplaced:
            return
            
        available_slots = []
        for row in config.PLAYER_DEPLOY_ROWS:
            for col in range(8):
                if not self.board.is_occupied(row, col):
                    available_slots.append((row, col))
                    
        for p in unplaced:
            if not available_slots:
                break # No more room on board
            row, col = available_slots.pop(0)
            self.board.place_piece(p, row, col)
            self.placed_pieces[p.id] = (row, col)
        
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
                    self.drag_source_pos = (row, col)
                    if self.dragging_piece.id in self.placed_pieces:
                        del self.placed_pieces[self.dragging_piece.id]
                    return
                    
        # Check if clicking on the unplaced roster sidebar
        self.drag_source_pos = None
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
                if row in config.PLAYER_DEPLOY_ROWS:
                    if not self.board.is_occupied(row, col):
                        self.board.place_piece(self.dragging_piece, row, col)
                        self.placed_pieces[self.dragging_piece.id] = (row, col)
                    else:
                        # Swap logic
                        resident_piece = self.board.grid[row][col]
                        if self.roster.get_piece(resident_piece.id):
                            # Detach resident piece
                            self.board.remove_piece(row, col)
                            del self.placed_pieces[resident_piece.id]
                            
                            # Place dragged piece
                            self.board.place_piece(self.dragging_piece, row, col)
                            self.placed_pieces[self.dragging_piece.id] = (row, col)
                            
                            # Check if the dragged piece came from the board (grid-to-grid swap)
                            if self.drag_source_pos:
                                src_row, src_col = self.drag_source_pos
                                self.board.place_piece(resident_piece, src_row, src_col)
                                self.placed_pieces[resident_piece.id] = (src_row, src_col)
                            # Else resident piece goes back to cursor/sidebar (effectively unplaced)
                else:
                    # Invalid row, snap back
                    if self.drag_source_pos:
                        src_row, src_col = self.drag_source_pos
                        self.board.place_piece(self.dragging_piece, src_row, src_col)
                        self.placed_pieces[self.dragging_piece.id] = (src_row, src_col)
            else:
                # Off-board drop, snap back
                if self.drag_source_pos:
                    src_row, src_col = self.drag_source_pos
                    self.board.place_piece(self.dragging_piece, src_row, src_col)
                    self.placed_pieces[self.dragging_piece.id] = (src_row, src_col)
                            
            self.dragging_piece = None
            self.drag_source_pos = None
            
    def clear_deployment(self):
        self.board.clear()
        self.placed_pieces.clear()
