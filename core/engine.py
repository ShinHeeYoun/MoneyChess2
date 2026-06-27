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
from ui.button import UIButton
from ui.animation_engine import AnimationEngine
from persistence.save_manager import SaveManager
from units.piece import PieceStatus

class GameEngine:
    def __init__(self, screen: pygame.Surface):
        self.window = screen
        self.screen = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self.state = GameState.MAIN_MENU
        self.running = True
        self.clock = pygame.time.Clock()
        
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
        self.current_stage = 1
        
        self.roster = RosterManager()
        self.economy = EconomyManager()
        self.shop_manager = ShopManager(self.economy, self.roster)
        
        self.board = BoardGrid()
        self.deployment_manager = DeploymentManager(self.board, self.roster)
        self.ai_generator = AIFormationGenerator(self.board)
        
        self.combat = CombatEngine(self.board, self.deployment_manager, self.ai_generator)
        self.hospital = CasualtyProcessor()
        self.anim_engine = AnimationEngine()
        
        self.casualty_results = []
        self.recruited_captives = []
        self.combat_reward = 0
        self.ai_turn_start_time = 0
        self.prev_ai_captures = 0
        self.prev_player_captures = 0
        
        self.buttons = []
        self.contract_previews = []
        self.selected_contract = None
        
        self.assets = {}
        self._load_assets()
        
        self.shop_manager.generate_shop()
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
                
    def _draw_piece(self, piece_type: str, is_player: bool, rect: pygame.Rect, lifted: bool = False):
        # Translate PieceType to filename prefix
        prefix = "w" if is_player else "b"
        key = f"{prefix}_{piece_type.lower()}"
        
        if key in self.assets:
            img = self.assets[key]
            if lifted:
                new_size = int(config.GRID_SQUARE_SIZE * 1.15)
                img = pygame.transform.scale(img, (new_size, new_size))
                img = img.copy()
                img.set_alpha(200)
                rect = img.get_rect(center=rect.center)
            self.screen.blit(img, rect)
        else:
            # Absolute fallback text if sprite is missing
            letter = self.font.render(piece_type[:1], True, config.TEXT_COLOR)
            self.screen.blit(letter, letter.get_rect(center=rect.center))

    def _build_ui_for_state(self):
        self.buttons.clear()
        
        if self.state == GameState.MAIN_MENU:
            self.buttons.append(UIButton(pygame.Rect(config.WINDOW_WIDTH//2 - 100, 300, 200, 50), "New Game", self.font, self.action_new_game))
            if os.path.exists(config.SAVE_FILE_PATH):
                self.buttons.append(UIButton(pygame.Rect(config.WINDOW_WIDTH//2 - 100, 370, 200, 50), "Load Game", self.font, self.action_load_game))
                
        elif self.state == GameState.MANAGEMENT:
            self.buttons.append(UIButton(pygame.Rect(50, 90, 200, 40), "Reroll Shop (-10g)", self.font, self.action_reroll))
            # Recruit Pawn Button
            recruit_cost = config.UNIT_DATA["Pawn"]["buy_cost"]
            rect = pygame.Rect(50, 420, 200, 40)
            self.buttons.append(UIButton(rect, f"Recruit Pawn ({recruit_cost}g)", self.small_font, self.action_buy_pawn))
            
            # Replenish Pawns Button
            repl_rect = pygame.Rect(50, 470, 200, 40)
            self.buttons.append(UIButton(repl_rect, "Replenish Pawns", self.small_font, self.action_replenish_pawns))
            
            self.buttons.append(UIButton(pygame.Rect(50, 600, 200, 50), "Proceed to Map", self.font, self.action_proceed_to_map))
            
            for i, piece_type in enumerate(self.shop_manager.current_shop):
                cost = config.UNIT_DATA[piece_type.value]["buy_cost"]
                rect = pygame.Rect(50, 180 + i * 40, 200, 30)
                text = f"Buy {piece_type.value} (-{cost}g)"
                self.buttons.append(UIButton(rect, text, self.small_font, self.action_buy_piece, (i,)))
                
            active = self.roster.get_active_units()
            
            # Grouping Logic for Aggregation
            grouped = {}
            for piece in active:
                if piece.piece_type.value == "King":
                    continue
                pt_val = piece.piece_type.value
                if pt_val not in grouped:
                    grouped[pt_val] = []
                grouped[pt_val].append(piece)
                
            sellable_index = 0
            for pt_val, pieces in grouped.items():
                if sellable_index >= 12:
                    break
                count = len(pieces)
                sample = pieces[0]
                rect = pygame.Rect(1000, 160 + sellable_index * 40, 250, 30)
                text = f"{pt_val} x{count} (Sell: +{sample.sell_value}g)"
                self.buttons.append(UIButton(rect, text, self.small_font, self.action_sell_piece, (sample.id,)))
                sellable_index += 1
                
            self.buttons.append(UIButton(pygame.Rect(1000, 600, 200, 50), "Next Stage", self.font, self.action_next_stage))
            
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
            self.buttons.append(UIButton(pygame.Rect(1000, 600, 200, 50), "Battle Start", self.font, self.action_start_combat))
            
        elif self.state == GameState.COMBAT:
            self.buttons.append(UIButton(pygame.Rect(1000, 600, 200, 50), "Retreat", self.font, self.action_retreat))
            
        elif self.state == GameState.RESOLUTION:
            self.buttons.append(UIButton(pygame.Rect(config.WINDOW_WIDTH//2 - 150, config.WINDOW_HEIGHT - 100, 300, 50), "Confirm & Proceed", self.font, self.action_return_to_camp))

    def action_new_game(self):
        from units.piece import PieceType, ChessPiece
        self.current_stage = 1
        self.economy.current_gold = config.STARTING_GOLD
        self.roster.pieces.clear()
        
        king = ChessPiece(PieceType.KING)
        self.roster.add_piece(king)
        self.deployment_manager.auto_deploy()
        
        self.shop_manager.generate_shop()
        self.state = GameState.MANAGEMENT
        self._build_ui_for_state()
        
    def action_load_game(self):
        self.current_stage = SaveManager.load_game(self.economy, self.roster)
        self.deployment_manager.auto_deploy()
        self.shop_manager.generate_shop()
        self.state = GameState.MANAGEMENT
        self._build_ui_for_state()
        
    def action_reroll(self):
        if self.shop_manager.reroll_shop():
            self._build_ui_for_state()
            
    def action_buy_piece(self, index):
        if self.economy.is_bankrupt:
            self.anim_engine.start_shake(10.0)
            return
            
        piece_type = self.shop_manager.current_shop[index]
        cost = config.UNIT_DATA[piece_type.value]["buy_cost"]
        if self.shop_manager.buy_piece(index):
            self.deployment_manager.auto_deploy()
            self.anim_engine.spawn_floating_text(150, 150 + index * 40, f"-{cost}g", self.font, (255, 50, 50))
            self._build_ui_for_state()
            
    def action_buy_pawn(self):
        if self.economy.is_bankrupt:
            self.anim_engine.start_shake(10.0)
            return
            
        pawns = [p for p in self.roster.get_active_units() if p.piece_type.value == "Pawn"]
        if len(pawns) >= 8:
            self.anim_engine.start_shake(5.0)
            return
            
        cost = config.UNIT_DATA["Pawn"]["buy_cost"]
        if self.economy.subtract_gold(cost):
            from units.piece import PieceType, ChessPiece
            new_pawn = ChessPiece(PieceType("Pawn"))
            self.roster.add_piece(new_pawn)
            self.deployment_manager.auto_deploy()
            self.anim_engine.spawn_floating_text(150, 400, f"-{cost}g", self.font, (255, 50, 50))
            self._build_ui_for_state()
            
    def action_replenish_pawns(self):
        if self.economy.is_bankrupt:
            self.anim_engine.start_shake(10.0)
            return
            
        pawns = [p for p in self.roster.get_active_units() if p.piece_type.value == "Pawn"]
        if len(pawns) >= 8:
            self.anim_engine.start_shake(5.0)
            return
            
        cost = config.UNIT_DATA["Pawn"]["buy_cost"]
        bought_count = 0
        while len(pawns) + bought_count < 8:
            if self.economy.subtract_gold(cost):
                from units.piece import PieceType, ChessPiece
                new_pawn = ChessPiece(PieceType("Pawn"))
                self.roster.add_piece(new_pawn)
                bought_count += 1
            else:
                break
                
        if bought_count > 0:
            self.deployment_manager.auto_deploy()
            self.anim_engine.spawn_floating_text(150, 450, f"-{cost * bought_count}g", self.font, (255, 50, 50))
            self._build_ui_for_state()
            
    def action_sell_piece(self, piece_id):
        piece = self.roster.get_piece(piece_id)
        if piece:
            val = piece.sell_value
            if self.shop_manager.sell_piece(piece_id):
                # We do not have the exact rect pos here easily, spawn near top of list
                self.anim_engine.spawn_floating_text(800, 250, f"+{val}g", self.font, (50, 255, 50))
                self._build_ui_for_state() # Crucial for Zero-Count Eviction
            
    def action_next_stage(self):
        if not self.economy.is_bankrupt:
            self.state = GameState.STAGE_SELECT
            self._build_ui_for_state()
            
    def action_proceed_to_map(self):
        self.state = GameState.STAGE_SELECT
        self._build_ui_for_state()
            
    def action_select_contract(self, index):
        self.selected_contract = self.contract_previews[index]
        self.state = GameState.DEPLOYMENT
        self.ai_generator.apply_formation(self.selected_contract["preview"])
        self._build_ui_for_state()
        
    def action_start_combat(self):
        # Validate King is deployed
        king_deployed = False
        for piece in self.deployment_manager.placed_pieces.keys():
            p = self.roster.get_piece(piece)
            if p and p.piece_type.value == "King":
                king_deployed = True
                break
                
        if not king_deployed:
            print("Cannot start combat: Commander (King) is not deployed!")
            self.anim_engine.start_shake(15.0)
            return
            
        if len(self.combat.get_ai_pieces_list()) == 0:
            print("WARNING: Zero enemy units detected! Forcing AI regeneration.")
            self.ai_generator.apply_formation(self.selected_contract["ai_preview"])

        self.state = GameState.COMBAT
        self.combat.start_combat()
        self.prev_ai_captures = 0
        self.prev_player_captures = 0
        self._build_ui_for_state()
        
    def action_retreat(self):
        if self.combat.outcome is None:
            self.combat.execute_retreat()
            
    def action_return_to_camp(self):
        if self.combat.outcome == "VICTORY":
            self.current_stage += 1
            
        self.roster.tick_hospital_turns()
        self.economy.process_upkeep(self.roster)
        
        act_count = len(self.roster.get_active_units())
        inj_count = len(self.roster.get_injured_units())
        ros_txt = self.font.render(f"Roster (Active: {act_count}, Injured: {inj_count})", True, config.TEXT_COLOR)
        self.screen.blit(ros_txt, (1000, 60))
        
        # King Status Visibility Guard
        king = None
        for p in self.roster.pieces:
            if p.piece_type.value == "King":
                king = p
                break
                
        if king:
            if king.status == PieceStatus.ACTIVE:
                status_str = "Status: ACTIVE"
                color = (150, 255, 150)
            else:
                status_str = f"Status: INJURED ({king.current_injury_turns} turns left)"
                color = (255, 150, 150)
            king_txt = self.small_font.render(f"Commander (King) - {status_str}", True, color)
            self.screen.blit(king_txt, (1000, 100))
            
        pygame.draw.line(self.screen, (100, 100, 100), (1000, 140), (1250, 140))
        
        if self.economy.current_gold <= 0 and act_count == 0 and inj_count == 0:
            self.state = GameState.GAME_OVER
        else:
            self.state = GameState.MANAGEMENT
            SaveManager.save_game(self.economy, self.roster, self.current_stage)
            self.shop_manager.generate_shop()
            
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
                if self.state in [GameState.DEPLOYMENT, GameState.MANAGEMENT]:
                    self.deployment_manager.handle_mouse_down(event.pos)
                elif self.state == GameState.COMBAT:
                    grid_pos = self.board.screen_to_grid(*event.pos)
                    if grid_pos:
                        self.combat.handle_mouse_down(grid_pos[0], grid_pos[1])
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.state in [GameState.DEPLOYMENT, GameState.MANAGEMENT]:
                    self.deployment_manager.handle_mouse_up(event.pos)
                elif self.state == GameState.COMBAT:
                    grid_pos = self.board.screen_to_grid(*event.pos)
                    if grid_pos:
                        self.combat.handle_mouse_up(grid_pos[0], grid_pos[1])

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
                self.recruited_captives = self.hospital.process_enemy_captives(self.combat.capture_buffer.captured_ai_units, self.roster)
                
                base_reward = self.selected_contract["reward"] if self.selected_contract else config.BASE_VICTORY_REWARD
                if self.combat.outcome == "VICTORY":
                    material_bonus = sum(config.MATERIAL_VALUES.get(p.piece_type.value, 0) for p in self.combat.capture_buffer.captured_ai_units)
                    self.combat_reward = base_reward + material_bonus
                else:
                    self.combat_reward = config.DEFEAT_REWARD
                    
                self.economy.add_gold(self.combat_reward)
                self.anim_engine.spawn_floating_text(config.WINDOW_WIDTH//2, config.WINDOW_HEIGHT//2, f"+{self.combat_reward}g", self.font, (255, 215, 0), 2.5)
                
                self.deployment_manager.clear_deployment()
                self.state = GameState.RESOLUTION
                self._build_ui_for_state()
                
            else:
                # Still in combat, check for captures to trigger screen shake
                cur_ai_caps = len(self.combat.capture_buffer.captured_ai_units)
                cur_player_caps = len(self.combat.capture_buffer.captured_player_units)
                if cur_ai_caps > self.prev_ai_captures or cur_player_caps > self.prev_player_captures:
                    self.anim_engine.start_shake(15.0)
                self.prev_ai_captures = cur_ai_caps
                self.prev_player_captures = cur_player_caps
                
        self.anim_engine.update(dt)
        
    def draw(self, dt: float = 1/60.0):
        self.screen.fill(config.BACKGROUND_COLOR)
        
        # Draw background panels
        pygame.draw.rect(self.screen, config.PANEL_COLOR, config.LEFT_PANEL_RECT)
        pygame.draw.rect(self.screen, config.PANEL_COLOR, config.RIGHT_PANEL_RECT)
        pygame.draw.rect(self.screen, config.PANEL_BORDER_COLOR, config.LEFT_PANEL_RECT, 2)
        pygame.draw.rect(self.screen, config.PANEL_BORDER_COLOR, config.RIGHT_PANEL_RECT, 2)
        
        if self.state == GameState.MANAGEMENT:
            self.draw_board(show_zones=True)
            self.draw_management_ui()
        elif self.state == GameState.STAGE_SELECT:
            self.draw_stage_select_ui()
        elif self.state in [GameState.DEPLOYMENT, GameState.COMBAT]:
            self.draw_board()
        elif self.state == GameState.RESOLUTION:
            # Draw board underneath
            self.draw_board()
            self.draw_resolution_ui()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over_ui()
            
        for btn in self.buttons:
            btn.draw(self.screen, dt)
            
        self.anim_engine.draw(self.screen)
            
        self.window.fill((0,0,0))
        self.window.blit(self.screen, self.anim_engine.get_shake_offset())
        pygame.display.flip()
        
    def draw_main_menu_ui(self):
        title = self.font.render("MoneyChess2", True, (255, 255, 255))
        self.screen.blit(title, (config.WINDOW_WIDTH // 2 - 100, 200))
        
        esc_quit = self.small_font.render("Press 'ESCAPE' to Quit", True, (255, 150, 150))
        self.screen.blit(esc_quit, (config.WINDOW_WIDTH // 2 - 100, 500))
        
    def draw_management_ui(self):
        stage_surf = self.font.render(f"Stage {self.current_stage}", True, (200, 200, 255))
        self.screen.blit(stage_surf, (1000, 20))
        
        color = (255, 100, 100) if self.economy.is_bankrupt else config.ACCENT_COLOR
        gold_surface = self.font.render(f"Gold: {self.economy.current_gold}", True, color)
        self.screen.blit(gold_surface, (20, 20))
        
        upkeep = self.economy.calculate_total_upkeep(self.roster)
        upkeep_surface = self.font.render(f"Upkeep: {upkeep}", True, (200, 200, 200))
        self.screen.blit(upkeep_surface, (20, 50))
        
        shop_title = self.font.render("Shop", True, config.TEXT_COLOR)
        self.screen.blit(shop_title, (20, 150))
            
        roster_title = self.font.render(f"Roster (Active: {len(self.roster.get_active_units())}, Injured: {len(self.roster.get_injured_units())})", True, config.TEXT_COLOR)
        self.screen.blit(roster_title, (1000, 60))
        
        # Lifted piece rendering for management dragging
        if self.deployment_manager.dragging_piece:
            mx, my = pygame.mouse.get_pos()
            rect = pygame.Rect(mx - config.GRID_SQUARE_SIZE//2, my - config.GRID_SQUARE_SIZE//2, config.GRID_SQUARE_SIZE, config.GRID_SQUARE_SIZE)
            self._draw_piece(self.deployment_manager.dragging_piece.piece_type.value, True, rect, lifted=True)
        
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
                
                color = config.COLOR_SQUARE_LIGHT if (row + col) % 2 == 0 else config.COLOR_SQUARE_DARK
                
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
                    
                    # Fog of War masking
                    mask_piece = False
                    if self.state == GameState.DEPLOYMENT and row in config.AI_DEPLOY_ROWS:
                        mask_piece = True
                        
                    if not mask_piece:
                        is_dragging_in_combat = (self.state == GameState.COMBAT and getattr(self.combat, "dragging_piece", None) == piece)
                        if not is_dragging_in_combat:
                            if self.state == GameState.COMBAT and piece.piece_type.value == "King":
                                if self.combat.is_king_guarded(is_player):
                                    aura = pygame.Surface((config.GRID_SQUARE_SIZE, config.GRID_SQUARE_SIZE), pygame.SRCALPHA)
                                    aura.fill((218, 165, 32, 120))
                                    self.screen.blit(aura, rect)
                                    
                            self._draw_piece(piece.piece_type.value, is_player, rect)
                
                # Draw grid boundary
                board_rect = pygame.Rect(config.BOARD_OFFSET_X, config.BOARD_OFFSET_Y, 8 * config.GRID_SQUARE_SIZE, 8 * config.GRID_SQUARE_SIZE)
                pygame.draw.rect(self.screen, (10, 10, 10), board_rect, 2)
                
                # Hover and Selection Highlight
                if hover_grid == (row, col) and (self.state in [GameState.DEPLOYMENT, GameState.COMBAT, GameState.MANAGEMENT]):
                    is_valid_hover = False
                    if self.state in [GameState.DEPLOYMENT, GameState.MANAGEMENT] and row in config.PLAYER_DEPLOY_ROWS and not self.board.is_occupied(row, col) and self.deployment_manager.dragging_piece:
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
            self._draw_piece(self.deployment_manager.dragging_piece.piece_type.value, True, rect, lifted=True)
            
    def draw_combat_ui(self):
        self.draw_board(show_zones=False)
        turn_text = "PLAYER TURN" if self.combat.is_player_turn else "AI TURN"
        turn_color = (150, 255, 150) if self.combat.is_player_turn else (255, 150, 150)
        turn_surf = self.font.render(turn_text, True, turn_color)
        self.screen.blit(turn_surf, (1000, 20))
        
        # Lifted piece rendering for combat dragging
        if getattr(self.combat, "dragging_piece", None):
            mx, my = pygame.mouse.get_pos()
            rect = pygame.Rect(mx - config.GRID_SQUARE_SIZE//2, my - config.GRID_SQUARE_SIZE//2, config.GRID_SQUARE_SIZE, config.GRID_SQUARE_SIZE)
            is_player = self.combat.is_player_piece(self.combat.dragging_piece)
            self._draw_piece(self.combat.dragging_piece.piece_type.value, is_player, rect, lifted=True)
        
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
        self.screen.blit(cas_title, (20, 100))
        
        y_offset = 130
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
            cas_surf = self.small_font.render(cas_str, True, color)
            self.screen.blit(cas_surf, (20, y_offset))
            y_offset += 25
            
        for piece in self.combat.dead_in_retreat:
            cas_str = f"{piece.piece_type.value} (ID: {str(piece.id)[:8]}...): DEAD - Abandoned in Retreat"
            cas_surf = self.small_font.render(cas_str, True, (255, 50, 50))
            self.screen.blit(cas_surf, (20, y_offset))
            y_offset += 25
            
        if self.recruited_captives:
            def_title = self.font.render("Defectors Recruited:", True, (100, 255, 100))
            self.screen.blit(def_title, (500, 100))
            def_y = 130
            for piece in self.recruited_captives:
                def_str = f"+ {piece.piece_type.value}"
                def_surf = self.small_font.render(def_str, True, (200, 255, 200))
                self.screen.blit(def_surf, (500, def_y))
                def_y += 25
        
    def draw_game_over_ui(self):
        msg1 = self.font.render("GAME OVER", True, (255, 0, 0))
        msg2 = self.font.render("Your company is bankrupt and has no remaining active or hospital units.", True, (200, 200, 200))
        self.screen.blit(msg1, (config.WINDOW_WIDTH // 2 - 100, config.WINDOW_HEIGHT // 2 - 40))
        self.screen.blit(msg2, (config.WINDOW_WIDTH // 2 - 400, config.WINDOW_HEIGHT // 2))

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events(pygame.event.get())
            self.update(dt)
            self.draw(dt)
