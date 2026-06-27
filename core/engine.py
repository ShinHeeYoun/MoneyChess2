import pygame
import os
import sys
from core.state import GameState
import config
from units.roster import RosterManager
from economy.economy_manager import EconomyManager
from economy.shop_generator import ShopManager
from deployment.board_grid import BoardGrid
from deployment.deployment_manager import DeploymentManager
from deployment.ai_formations import AIFormationGenerator
from combat.combat_engine import CombatEngine
from casualty.hospital_system import CasualtyProcessor
from persistence.save_manager import SaveManager
from ui.button import UIButton

class GameEngine:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.state = GameState.MAIN_MENU
        self.running = True
        
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
        self.current_stage = 1
        
        self.roster = RosterManager()
        self.economy = EconomyManager()
        self.shop = ShopManager(self.economy, self.roster)
        
        self.board = BoardGrid()
        self.deployment_manager = DeploymentManager(self.board, self.roster)
        self.ai_generator = AIFormationGenerator(self.board)
        
        self.combat = CombatEngine(self.board, self.deployment_manager, self.ai_generator)
        self.hospital = CasualtyProcessor()
        
        self.casualty_results = []
        self.combat_reward = 0
        self.ai_turn_start_time = 0
        
        self.buttons = []
        self.contract_previews = []
        self.selected_contract = None
        
        self.assets = {}
        self._load_assets()
        
        self.shop.generate_shop()
        self._build_ui_for_state()
        
    def _load_assets(self):
        if not os.path.exists(config.ASSETS_DIR):
            try:
                os.makedirs(config.ASSETS_DIR)
            except:
                pass
                
        expected_files = [
            "w_pawn.png", "w_knight.png", "w_bishop.png", "w_rook.png", "w_queen.png", "w_king.png",
            "b_pawn.png", "b_knight.png", "b_bishop.png", "b_rook.png", "b_queen.png", "b_king.png"
        ]
        
        missing = []
        for filename in expected_files:
            path = os.path.join(config.ASSETS_DIR, filename)
            if os.path.exists(path):
                # We strip the extension to create the key
                key = filename.split('.')[0]
                img = pygame.image.load(path).convert_alpha()
                # Scale it to fit the grid
                img = pygame.transform.scale(img, (config.GRID_SQUARE_SIZE, config.GRID_SQUARE_SIZE))
                self.assets[key] = img
            else:
                missing.append(filename)
                
        if missing:
            print(f"WARNING: The following asset files are missing from {config.ASSETS_DIR}:")
            for m in missing:
                print(f"  - {m}")
                
    def _draw_piece(self, piece_type: str, is_player: bool, rect: pygame.Rect):
        # Translate PieceType to filename prefix
        prefix = "w" if is_player else "b"
        key = f"{prefix}_{piece_type.lower()}"
        
        if key in self.assets:
            self.screen.blit(self.assets[key], rect)
        else:
            # Absolute fallback text if sprite is missing
            letter = self.font.render(piece_type[:1], True, (255, 255, 255))
            self.screen.blit(letter, letter.get_rect(center=rect.center))

    def _build_ui_for_state(self):
        self.buttons.clear()
        
        if self.state == GameState.MAIN_MENU:
            self.buttons.append(UIButton(pygame.Rect(config.WINDOW_WIDTH//2 - 100, 300, 200, 50), "New Game", self.font, self.action_new_game))
            if os.path.exists(config.SAVE_FILE_PATH):
                self.buttons.append(UIButton(pygame.Rect(config.WINDOW_WIDTH//2 - 100, 370, 200, 50), "Load Game", self.font, self.action_load_game))
                
        elif self.state == GameState.MANAGEMENT:
            self.buttons.append(UIButton(pygame.Rect(20, 110, 200, 30), f"Reroll ({config.SHOP_REROLL_COST}g)", self.small_font, self.action_reroll))
            
            # Unlimited Pawn Button
            pawn_cost = config.UNIT_DATA["Pawn"]["buy_cost"]
            self.buttons.append(UIButton(pygame.Rect(240, 110, 200, 30), f"Recruit Pawn ({pawn_cost}g)", self.small_font, self.action_buy_pawn))
            
            for i, piece_type in enumerate(self.shop.current_shop):
                cost = config.UNIT_DATA[piece_type.value]["buy_cost"]
                rect = pygame.Rect(20, 150 + i * 40, 200, 30)
                self.buttons.append(UIButton(rect, f"Buy {piece_type.value} ({cost}g)", self.small_font, self.action_buy_piece, (i,)))
            
            active = self.roster.get_active_units()
            sellable_index = 0
            for piece in active:
                if piece.piece_type.value == "King":
                    continue
                if sellable_index >= 10:
                    break
                rect = pygame.Rect(700, 150 + sellable_index * 40, 200, 30)
                self.buttons.append(UIButton(rect, f"Sell {piece.piece_type.value} (+{piece.sell_value}g)", self.small_font, self.action_sell_piece, (piece.id,)))
                sellable_index += 1
                
            self.buttons.append(UIButton(pygame.Rect(config.WINDOW_WIDTH - 200, config.WINDOW_HEIGHT - 80, 150, 40), "Next Stage", self.font, self.action_next_stage))
            
        elif self.state == GameState.STAGE_SELECT:
            self.contract_previews = []
            keys = list(config.CONTRACTS.keys())
            for i, c_key in enumerate(keys):
                contract = config.CONTRACTS[c_key]
                preview = self.ai_generator.generate_formation_preview(self.current_stage, contract["budget_mult"])
                reward = int(config.BASE_VICTORY_REWARD * contract["reward_mult"])
                self.contract_previews.append({"key": c_key, "preview": preview, "reward": reward})
                
                # Format text summary
                summary = []
                for pt, count in preview["counts"].items():
                    summary.append(f"{count} {pt}s")
                summary_str = "\n".join(summary)
                if not summary_str:
                    summary_str = "None"
                    
                text = f"{contract['name']}\n\nExpected Forces:\n{summary_str}\n\nReward: {reward}g\n\nClick to Select"
                rect = pygame.Rect(150 + i * 350, 150, 300, 400)
                btn = UIButton(rect, text, self.small_font, self.action_select_contract, (i,))
                self.buttons.append(btn)
                
        elif self.state == GameState.DEPLOYMENT:
            self.buttons.append(UIButton(pygame.Rect(config.WINDOW_WIDTH - 250, config.WINDOW_HEIGHT - 80, 200, 50), "Battle Start", self.font, self.action_start_combat))
            
        elif self.state == GameState.RESOLUTION:
            self.buttons.append(UIButton(pygame.Rect(config.WINDOW_WIDTH//2 - 150, config.WINDOW_HEIGHT - 100, 300, 50), "Confirm & Proceed", self.font, self.action_return_to_camp))

    def action_new_game(self):
        from units.piece import PieceType, ChessPiece
        self.current_stage = 1
        self.economy.current_gold = config.STARTING_GOLD
        self.roster.pieces.clear()
        
        # The King is the company commander; must be added initially
        king = ChessPiece(PieceType.KING)
        self.roster.add_piece(king)
        
        self.shop.generate_shop()
        self.state = GameState.MANAGEMENT
        self._build_ui_for_state()
        
    def action_load_game(self):
        self.current_stage = SaveManager.load_game(self.economy, self.roster)
        self.shop.generate_shop()
        self.state = GameState.MANAGEMENT
        self._build_ui_for_state()
        
    def action_reroll(self):
        if self.shop.reroll_shop():
            self._build_ui_for_state()
            
    def action_buy_piece(self, index):
        if self.shop.buy_piece(index):
            self._build_ui_for_state()
            
    def action_buy_pawn(self):
        from units.piece import PieceType, ChessPiece
        pawn_cost = config.UNIT_DATA["Pawn"]["buy_cost"]
        if not self.economy.is_bankrupt and self.economy.subtract_gold(pawn_cost):
            piece = ChessPiece(PieceType.PAWN)
            self.roster.add_piece(piece)
            self._build_ui_for_state()
            
    def action_sell_piece(self, piece_id):
        if self.shop.sell_piece(piece_id):
            self._build_ui_for_state()
            
    def action_next_stage(self):
        if not self.economy.is_bankrupt:
            self.state = GameState.STAGE_SELECT
            self._build_ui_for_state()
            
    def action_select_contract(self, index):
        self.selected_contract = self.contract_previews[index]
        self.state = GameState.DEPLOYMENT
        self.deployment_manager.auto_deploy()
        self.ai_generator.apply_formation(self.selected_contract["preview"])
        self._build_ui_for_state()
        
    def action_start_combat(self):
        # Deployment Guard: King Requirement
        placed_pids = self.deployment_manager.placed_pieces.keys()
        placed_pieces = [self.roster.get_piece(pid) for pid in placed_pids]
        
        has_king = False
        for p in placed_pieces:
            if p and p.piece_type.value == "King":
                has_king = True
                break
                
        if not has_king:
            print("DEPLOYMENT WARNING: You must deploy your King on the active grid before commencing battle!")
            return
            
        # Fallback Check: Ensure AI pieces populate the board
        if not self.ai_generator.ai_pieces:
            print("FALLBACK: Regenerating AI Formation")
            if self.selected_contract:
                self.ai_generator.apply_formation(self.selected_contract["preview"])
            
        self.state = GameState.COMBAT
        self.combat.start_combat()
        self._build_ui_for_state()
        
    def action_return_to_camp(self):
        if self.combat.outcome == "VICTORY":
            self.current_stage += 1
            
        self.roster.tick_hospital_turns()
        self.economy.process_upkeep(self.roster)
        
        active_count = len(self.roster.get_active_units())
        injured_count = len(self.roster.get_injured_units())
        if self.economy.current_gold <= 0 and active_count == 0 and injured_count == 0:
            self.state = GameState.GAME_OVER
        else:
            self.state = GameState.MANAGEMENT
            SaveManager.save_game(self.economy, self.roster, self.current_stage)
            self.shop.generate_shop()
            
        self._build_ui_for_state()

    def quit_game(self):
        self.running = False
        pygame.quit()
        sys.exit()
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()
                    
            # Handle UI buttons globally
            handled = False
            for btn in self.buttons:
                if btn.handle_event(event):
                    handled = True
                    break
                    
            if handled:
                continue
                
            # State specific mouse events
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.state == GameState.DEPLOYMENT:
                    self.deployment_manager.handle_mouse_down(event.pos)
                elif self.state == GameState.COMBAT:
                    grid_pos = self.board.screen_to_grid(*event.pos)
                    if grid_pos:
                        self.combat.handle_click(grid_pos[0], grid_pos[1])
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.state == GameState.DEPLOYMENT:
                    self.deployment_manager.handle_mouse_up(event.pos)

    def update(self, dt: float):
        if self.state == GameState.COMBAT:
            if not self.combat.is_player_turn and not self.combat.outcome:
                if self.ai_turn_start_time == 0:
                    self.ai_turn_start_time = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - self.ai_turn_start_time >= 500:
                    self.combat.execute_ai_turn()
                    self.ai_turn_start_time = 0
            
            if self.combat.outcome:
                self.casualty_results = self.hospital.process_casualties(self.combat.capture_buffer.captured_player_units, self.roster)
                if self.combat.outcome == "VICTORY":
                    # Use contract multiplier
                    base_reward = self.selected_contract["reward"] if self.selected_contract else config.BASE_VICTORY_REWARD
                    self.combat_reward = base_reward
                else:
                    self.combat_reward = config.DEFEAT_REWARD
                self.economy.add_gold(self.combat_reward)
                
                self.deployment_manager.clear_deployment()
                self.state = GameState.RESOLUTION
                self._build_ui_for_state()
        
    def draw(self):
        self.screen.fill((30, 30, 30))
        
        if self.state == GameState.MAIN_MENU:
            self.draw_main_menu_ui()
        elif self.state == GameState.MANAGEMENT:
            self.draw_management_ui()
        elif self.state == GameState.STAGE_SELECT:
            self.draw_stage_select_ui()
        elif self.state == GameState.DEPLOYMENT:
            self.draw_deployment_ui()
        elif self.state == GameState.COMBAT:
            self.draw_combat_ui()
        elif self.state == GameState.RESOLUTION:
            self.draw_resolution_ui()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over_ui()
            
        # Draw buttons
        for btn in self.buttons:
            btn.draw(self.screen)
            
        pygame.display.flip()
        
    def draw_main_menu_ui(self):
        title = self.font.render("MoneyChess2", True, (255, 255, 255))
        self.screen.blit(title, (config.WINDOW_WIDTH // 2 - 100, 200))
        
        esc_quit = self.small_font.render("Press 'ESCAPE' to Quit", True, (255, 150, 150))
        self.screen.blit(esc_quit, (config.WINDOW_WIDTH // 2 - 100, 500))
        
    def draw_management_ui(self):
        stage_surf = self.font.render(f"Stage {self.current_stage}", True, (200, 200, 255))
        self.screen.blit(stage_surf, (config.WINDOW_WIDTH - 200, 20))
        
        color = (255, 100, 100) if self.economy.is_bankrupt else (255, 255, 100)
        gold_surface = self.font.render(f"Gold: {self.economy.current_gold}", True, color)
        self.screen.blit(gold_surface, (20, 20))
        
        upkeep = self.economy.calculate_total_upkeep(self.roster)
        upkeep_surface = self.font.render(f"Upkeep: {upkeep}", True, (200, 200, 200))
        self.screen.blit(upkeep_surface, (20, 60))
        
        shop_title = self.font.render("Shop", True, (255, 255, 255))
        self.screen.blit(shop_title, (20, 120))
            
        roster_title = self.font.render(f"Roster (Active: {len(self.roster.get_active_units())}, Injured: {len(self.roster.get_injured_units())})", True, (255, 255, 255))
        self.screen.blit(roster_title, (700, 120))
        
    def draw_stage_select_ui(self):
        title = self.font.render("Select Tactical Contract", True, (255, 255, 255))
        self.screen.blit(title, (config.WINDOW_WIDTH // 2 - 150, 50))
            
    def draw_board(self, show_zones=False):
        mx, my = pygame.mouse.get_pos()
        hover_grid = self.board.screen_to_grid(mx, my)
        
        for row in range(8):
            for col in range(8):
                x = config.BOARD_OFFSET_X + col * config.GRID_SQUARE_SIZE
                y = config.BOARD_OFFSET_Y + row * config.GRID_SQUARE_SIZE
                
                color = (200, 200, 200) if (row + col) % 2 == 0 else (100, 100, 100)
                
                if show_zones:
                    if row in config.PLAYER_DEPLOY_ROWS:
                        color = (color[0], color[1], color[2] + 50) if color[2] <= 205 else color
                    elif row in config.AI_DEPLOY_ROWS:
                        color = (color[0] + 50, color[1], color[2]) if color[0] <= 205 else color
                        
                if self.state == GameState.COMBAT:
                    if self.combat.selected_pos == (row, col):
                        color = (255, 255, 100)
                    elif (row, col) in self.combat.valid_moves:
                        color = (150, 255, 150)
                        
                rect = pygame.Rect(x, y, config.GRID_SQUARE_SIZE, config.GRID_SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                
                if self.board.is_occupied(row, col):
                    piece = self.board.grid[row][col]
                    is_player = self.combat.is_player_piece(piece) or (self.state == GameState.DEPLOYMENT and self.deployment_manager.roster.get_piece(piece.id))
                    self._draw_piece(piece.piece_type.value, is_player, rect)
                
                # Hover and Selection Highlight
                if hover_grid == (row, col) and (self.state in [GameState.DEPLOYMENT, GameState.COMBAT]):
                    is_valid_hover = False
                    if self.state == GameState.DEPLOYMENT and row in config.PLAYER_DEPLOY_ROWS and not self.board.is_occupied(row, col) and self.deployment_manager.dragging_piece:
                        is_valid_hover = True
                    elif self.state == GameState.COMBAT:
                        if self.combat.selected_pos and (row, col) in self.combat.valid_moves:
                            is_valid_hover = True
                        elif not self.combat.selected_pos and self.board.is_occupied(row, col) and self.combat.is_player_piece(self.board.grid[row][col]):
                            is_valid_hover = True
                            
                    if is_valid_hover:
                        overlay = pygame.Surface((config.GRID_SQUARE_SIZE, config.GRID_SQUARE_SIZE), pygame.SRCALPHA)
                        overlay.fill((255, 255, 0, 100))
                        self.screen.blit(overlay, rect)
                    
    def draw_deployment_ui(self):
        self.draw_board(show_zones=True)
                    
        sidebar_title = self.font.render("Unplaced Units", True, (255, 255, 255))
        self.screen.blit(sidebar_title, (20, 150))
        
        sidebar_x = 20
        sidebar_y_start = 200
        unplaced = self.deployment_manager.get_unplaced_active_units()
        for i, piece in enumerate(unplaced):
            if self.deployment_manager.dragging_piece and self.deployment_manager.dragging_piece.id == piece.id:
                continue
            rect = pygame.Rect(sidebar_x, sidebar_y_start + i * 40, 150, 30)
            pygame.draw.rect(self.screen, (100, 150, 200), rect)
            label = self.small_font.render(piece.piece_type.value, True, (0, 0, 0))
            self.screen.blit(label, (sidebar_x + 5, sidebar_y_start + i * 40 + 5))
            
        if self.deployment_manager.dragging_piece:
            mx, my = pygame.mouse.get_pos()
            rect = pygame.Rect(mx - config.GRID_SQUARE_SIZE//2, my - config.GRID_SQUARE_SIZE//2, config.GRID_SQUARE_SIZE, config.GRID_SQUARE_SIZE)
            self._draw_piece(self.deployment_manager.dragging_piece.piece_type.value, True, rect)
        
    def draw_combat_ui(self):
        self.draw_board(show_zones=False)
        turn_text = "PLAYER TURN" if self.combat.is_player_turn else "AI TURN"
        turn_color = (150, 255, 150) if self.combat.is_player_turn else (255, 150, 150)
        turn_surf = self.font.render(turn_text, True, turn_color)
        self.screen.blit(turn_surf, (20, 20))
        
    def draw_resolution_ui(self):
        self.draw_combat_ui()
        
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        title = self.font.render(f"COMBAT RESOLUTION: {self.combat.outcome}", True, (255, 255, 255))
        self.screen.blit(title, (20, 20))
        
        reward_txt = self.font.render(f"Gold Gained: {self.combat_reward}", True, (255, 255, 0))
        self.screen.blit(reward_txt, (20, 60))
        
        cas_title = self.font.render("Casualty Report:", True, (200, 200, 200))
        self.screen.blit(cas_title, (20, 120))
        
        for i, (piece, outcome) in enumerate(self.casualty_results):
            if outcome == "HEALTHY":
                color = (150, 255, 150)
                info = "Returned safely"
            elif outcome == "INJURED":
                color = (255, 200, 100)
                info = f"Unusable for {piece.current_injury_turns} turn(s)"
            else:
                color = (255, 100, 100)
                info = "Removed from company"
                
            cas_str = f"{piece.piece_type.value} (ID: {str(piece.id)[:8]}...): {outcome} - {info}"
            cas_surf = self.font.render(cas_str, True, color)
            self.screen.blit(cas_surf, (20, 160 + i * 40))
        
    def draw_game_over_ui(self):
        msg1 = self.font.render("GAME OVER", True, (255, 0, 0))
        msg2 = self.font.render("Your company is bankrupt and has no remaining active or hospital units.", True, (200, 200, 200))
        self.screen.blit(msg1, (config.WINDOW_WIDTH // 2 - 100, config.WINDOW_HEIGHT // 2 - 40))
        self.screen.blit(msg2, (config.WINDOW_WIDTH // 2 - 400, config.WINDOW_HEIGHT // 2))
