import pygame
from core.state import GameState
import config
from units.roster import RosterManager
from economy.economy_manager import EconomyManager
from economy.shop_generator import ShopManager

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
        
        self.shop.generate_shop()
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.MANAGEMENT:
                    self.handle_management_input(event)
                    
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
        pass
        
    def draw(self):
        self.screen.fill((30, 30, 30))
        
        if self.state == GameState.MANAGEMENT:
            self.draw_management_ui()
            
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
