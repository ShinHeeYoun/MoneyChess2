import pygame
import config

class UIButton:
    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font, callback=None, callback_args=None):
        self.rect = rect
        self.text = text
        self.font = font
        self.callback = callback
        self.callback_args = callback_args if callback_args else ()
        self.is_hovered = False
        
    def draw(self, surface: pygame.Surface):
        color = config.BUTTON_COLOR_HOVER if self.is_hovered else config.BUTTON_COLOR_NEUTRAL
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2)
        
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
