import pygame

class Button:
    """A clickable rectangle button with hover highlighting and shadows."""

    def __init__(self, x, y, width, height, text, font, text_color, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen, mouse_pos):
        # Draw a subtle drop shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y += 3
        pygame.draw.rect(screen, (130, 130, 130), shadow_rect, border_radius=8)

        # Draw the main button body
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        # Draw a border around the button
        pygame.draw.rect(screen, (80, 80, 80), self.rect, width=2, border_radius=8)

        # Draw the text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False