import pygame
import sys
import config
from core.engine import GameEngine

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption("MoneyChess2")
    
    clock = pygame.time.Clock()
    engine = GameEngine(screen)
    
    while engine.running:
        dt = clock.tick(config.FPS_LIMIT) / 1000.0
        events = pygame.event.get()
        
        engine.handle_events(events)
        engine.update(dt)
        engine.draw()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
