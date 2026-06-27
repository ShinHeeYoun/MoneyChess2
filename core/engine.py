import pygame
from core.state import GameState
import config
from units.roster import RosterManager
from economy.economy_manager import EconomyManager
from economy.shop_generator import ShopManager
from deployment.board_grid import BoardGrid
from deployment.deployment_manager import DeploymentManager
from deployment.ai_formations import AIFormationGenerator

class GameEngine:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.state = GameState.MANAGEMENT # start in management for now
        self.running = True
        
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 36)
        
        # Initialize modules
        self.roster = RosterManager()
        self.economy = EconomyManager()
        self.shop = ShopManager(self.economy, self.roster)
        
        self.board = BoardGrid()
        self.deployment_manager = DeploymentManager(self.board, self.roster)
        self.ai_generator = AIFormationGenerator(self.board)
        
        self.shop.generate_shop()
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.transition_state()
                elif self.state == GameState.MANAGEMENT:
                    self.handle_management_input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.DEPLOYMENT:
                    if event.button == 1: # Left click
                        self.deployment_manager.handle_mouse_down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.state == GameState.DEPLOYMENT:
                    if event.button == 1:
                        self.deployment_manager.handle_mouse_up(event.pos)
                        
    def transition_state(self):
        if self.state == GameState.MANAGEMENT:
            if not self.economy.is_bankrupt:
                self.state = GameState.DEPLOYMENT
                print("Transitioned to DEPLOYMENT")
                self.ai_generator.generate_formation()
            else:
                print("Cannot deploy while bankrupt!")
        elif self.state == GameState.DEPLOYMENT:
            self.state = GameState.COMBAT
            print("Transitioned to COMBAT")
                    
    def handle_management_input(self, event):
        if event.key == pygame.K_r:
            success = self.shop.reroll_shop()
            if success:
                print("Shop rerolled!")
            else:
                print("Failed to reroll. Bankrupt or insufficient gold.")
        elif event.key == pygame.K_1:
            self._try_buy(0)
        elif event.key == pygame.K_2:
            self._try_buy(1)
        elif event.key == pygame.K_3:
            self._try_buy(2)
        elif event.key == pygame.K_4:
            self._try_buy(3)
        elif event.key == pygame.K_5:
            self._try_buy(4)
        elif event.key == pygame.K_s:
            # Sell the first active piece for testing
            active = self.roster.get_active_units()
            if active:
                self.shop.sell_piece(active[0].id)
                print(f"Sold piece: {active[0].piece_type.value}")
        elif event.key == pygame.K_u:
            # Process upkeep manually for testing
            self.economy.process_upkeep(self.roster)
            print("Upkeep processed.")

    def _try_buy(self, index):
        success = self.shop.buy_piece(index)
        if success:
            print(f"Bought piece at slot {index + 1}!")
        else:
            print(f"Failed to buy piece at slot {index + 1}.")
                
    def update(self, dt: float):
        if self.state == GameState.DEPLOYMENT:
            # Use mouse position from pygame directly for drag visuals
            pass
        
    def draw(self):
        self.screen.fill((30, 30, 30))
        
        if self.state == GameState.MANAGEMENT:
            self.draw_management_ui()
        elif self.state == GameState.DEPLOYMENT:
            self.draw_deployment_ui()
            
        pygame.display.flip()
        
    def draw_management_ui(self):
        # Render gold and status
        color = (255, 100, 100) if self.economy.is_bankrupt else (255, 255, 100)
        gold_surface = self.font.render(f"Gold: {self.economy.current_gold}", True, color)
        self.screen.blit(gold_surface, (20, 20))
        
        upkeep = self.economy.calculate_total_upkeep(self.roster)
        upkeep_surface = self.font.render(f"Upkeep: {upkeep}", True, (200, 200, 200))
        self.screen.blit(upkeep_surface, (20, 60))
        
        # Render shop
        shop_title = self.font.render("Shop (Press 1-5 to buy, R to reroll, S to sell first unit, U to process upkeep)", True, (255, 255, 255))
        self.screen.blit(shop_title, (20, 120))
        
        for i, piece_type in enumerate(self.shop.current_shop):
            cost = config.UNIT_DATA[piece_type.value]["buy_cost"]
            item_surf = self.font.render(f"{i+1}: {piece_type.value} ({cost}g)", True, (150, 255, 150))
            self.screen.blit(item_surf, (40, 160 + i * 40))
            
        # Render Roster
        roster_title = self.font.render(f"Roster (Active: {len(self.roster.get_active_units())})", True, (255, 255, 255))
        self.screen.blit(roster_title, (400, 120))
        
        for i, piece in enumerate(self.roster.get_active_units()[:10]): # Show up to 10
            piece_surf = self.font.render(f"{piece.piece_type.value} (Sell: {piece.sell_value}g)", True, (150, 150, 255))
            self.screen.blit(piece_surf, (420, 160 + i * 40))
            
        enter_msg = self.font.render("Press ENTER to proceed to Deployment", True, (200, 255, 200))
        self.screen.blit(enter_msg, (20, config.WINDOW_HEIGHT - 50))
            
    def draw_deployment_ui(self):
        # Draw 8x8 Grid
        for row in range(8):
            for col in range(8):
                x = config.BOARD_OFFSET_X + col * config.GRID_SQUARE_SIZE
                y = config.BOARD_OFFSET_Y + row * config.GRID_SQUARE_SIZE
                
                # Checkered pattern
                color = (200, 200, 200) if (row + col) % 2 == 0 else (100, 100, 100)
                
                # Highlight player deploy zone
                if row in config.PLAYER_DEPLOY_ROWS:
                    color = (color[0], color[1], color[2] + 50) if color[2] <= 205 else color
                # Highlight AI deploy zone
                elif row in config.AI_DEPLOY_ROWS:
                    color = (color[0] + 50, color[1], color[2]) if color[0] <= 205 else color
                    
                pygame.draw.rect(self.screen, color, (x, y, config.GRID_SQUARE_SIZE, config.GRID_SQUARE_SIZE))
                
                # Draw pieces on board
                if self.board.is_occupied(row, col):
                    piece = self.board.grid[row][col]
                    piece_surf = self.font.render(piece.piece_type.value[:2], True, (0, 0, 0))
                    self.screen.blit(piece_surf, (x + 20, y + 25))
                    
        # Draw Sidebar (Unplaced Units)
        sidebar_title = self.font.render("Unplaced Units", True, (255, 255, 255))
        self.screen.blit(sidebar_title, (20, 150))
        
        sidebar_x = 20
        sidebar_y_start = 200
        unplaced = self.deployment_manager.get_unplaced_active_units()
        for i, piece in enumerate(unplaced):
            # Skip drawing the one we are dragging
            if self.deployment_manager.dragging_piece and self.deployment_manager.dragging_piece.id == piece.id:
                continue
            rect = pygame.Rect(sidebar_x, sidebar_y_start + i * 40, 150, 30)
            pygame.draw.rect(self.screen, (100, 150, 200), rect)
            label = self.font.render(piece.piece_type.value, True, (0, 0, 0))
            self.screen.blit(label, (sidebar_x + 5, sidebar_y_start + i * 40 + 5))
            
        # Draw Dragging Piece
        if self.deployment_manager.dragging_piece:
            mx, my = pygame.mouse.get_pos()
            # Simple text representation at mouse
            drag_label = self.font.render(self.deployment_manager.dragging_piece.piece_type.value, True, (255, 255, 0))
            self.screen.blit(drag_label, (mx - 20, my - 15))
            
        enter_msg = self.font.render("Press ENTER to proceed to Combat", True, (200, 255, 200))
        self.screen.blit(enter_msg, (config.BOARD_OFFSET_X, config.WINDOW_HEIGHT - 40))
