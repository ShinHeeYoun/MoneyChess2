import pygame
import config

class UIButton:
    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font, callback=None, callback_args=None):
        self.rect = rect
        self.text = text
        self.font = font
        self.callback = callback
        self.callback_args = callback_args if callback_args else ()
        self.is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        self.hover_factor = 0.0
        
    def _lerp_color(self, c1, c2, t):
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t)
        )
        
    def draw(self, surface: pygame.Surface, dt: float = 1/60.0):
        # Update hover_factor
        if self.is_hovered:
            self.hover_factor = min(1.0, self.hover_factor + dt * 5.0) # Reach 1.0 in ~0.2s
        else:
            self.hover_factor = max(0.0, self.hover_factor - dt * 5.0)
            
        color = self._lerp_color(config.BUTTON_COLOR_NEUTRAL, config.BUTTON_COLOR_HOVER, self.hover_factor)
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        
        # Alpha blended hover border
        if self.hover_factor > 0:
            border_color = self._lerp_color((100, 100, 100), (200, 200, 200), self.hover_factor)
            pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=6)
        else:
            pygame.draw.rect(surface, (80, 80, 80), self.rect, 2, border_radius=6)
        
        # Text rendering
        lines = self.text.split('\n')
        total_height = len(lines) * self.font.get_linesize()
        start_y = self.rect.centery - (total_height // 2)
        
        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, config.BUTTON_TEXT_COLOR)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, start_y + i * self.font.get_linesize() + (self.font.get_linesize()//2)))
            surface.blit(text_surf, text_rect)
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                if self.callback:
                    self.callback(*self.callback_args)
                return True
        return False
