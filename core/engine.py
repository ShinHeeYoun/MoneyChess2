import pygame
from core.state import GameState
import config

class GameEngine:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.state = GameState.MAIN_MENU
        self.running = True
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                
    def update(self, dt: float):
        # State routing logic will go here
        pass
        
    def draw(self):
        self.screen.fill((30, 30, 30)) # Dark gray background
        
        # State-specific rendering will go here
        
        pygame.display.flip()
