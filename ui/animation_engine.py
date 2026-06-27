import pygame
import random

class FloatingText:
    def __init__(self, x: int, y: int, text: str, font: pygame.font.Font, color: tuple, lifetime: float = 1.5):
        self.x = x
        self.y = float(y)
        self.text = text
        self.font = font
        self.color = color
        self.max_lifetime = lifetime
        self.lifetime = lifetime
        
    def update(self, dt: float):
        self.lifetime -= dt
        self.y -= 20 * dt  # Drift upwards
        
    def draw(self, surface: pygame.Surface):
        if self.lifetime <= 0:
            return
            
        alpha = int(255 * max(0, self.lifetime / self.max_lifetime))
        text_surf = self.font.render(self.text, True, self.color)
        text_surf.set_alpha(alpha)
        
        rect = text_surf.get_rect(center=(self.x, int(self.y)))
        surface.blit(text_surf, rect)

class AnimationEngine:
    def __init__(self):
        self.floating_texts = []
        self.shake_intensity = 0.0
        self.shake_decay = 50.0 # Intensity lost per second
        
    def spawn_floating_text(self, x: int, y: int, text: str, font: pygame.font.Font, color: tuple, lifetime: float = 1.5):
        self.floating_texts.append(FloatingText(x, y, text, font, color, lifetime))
        
    def start_shake(self, intensity: float):
        self.shake_intensity = intensity
        
    def update(self, dt: float):
        # Update floating texts
        for ft in self.floating_texts:
            ft.update(dt)
        # Purge expired
        self.floating_texts = [ft for ft in self.floating_texts if ft.lifetime > 0]
        
        # Update shake
        if self.shake_intensity > 0:
            self.shake_intensity -= self.shake_decay * dt
            if self.shake_intensity < 0:
                self.shake_intensity = 0
                
    def get_shake_offset(self):
        if self.shake_intensity <= 0:
            return (0, 0)
        dx = random.uniform(-self.shake_intensity, self.shake_intensity)
        dy = random.uniform(-self.shake_intensity, self.shake_intensity)
        return (int(dx), int(dy))
        
    def draw(self, surface: pygame.Surface):
        for ft in self.floating_texts:
            ft.draw(surface)
