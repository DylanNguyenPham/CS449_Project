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
        shadow_rect = self.rect.copy()
        shadow_rect.y += 3
        pygame.draw.rect(screen, (130, 130, 130), shadow_rect, border_radius=8)

        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        pygame.draw.rect(screen, (80, 80, 80), self.rect, width=2, border_radius=8)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False


class Dropdown:
    """A dropdown menu component for selecting game options."""

    def __init__(self, x, y, width, height, label, options, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.options = options
        self.font = font
        self.selected_index = 0
        self.is_open = False
        self.option_rects = []

    def get_selected(self):
        return self.options[self.selected_index]

    def draw(self, screen, mouse_pos):
        bg_color = (210, 210, 210) if self.rect.collidepoint(mouse_pos) else (230, 230, 230)
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=6)
        pygame.draw.rect(screen, (80, 80, 80), self.rect, width=2, border_radius=6)

        display_text = f"{self.label}: {self.get_selected()}"
        text_surf = self.font.render(display_text, True, (30, 30, 30))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

        arrow_text = "▲" if self.is_open else "▼"
        arrow_surf = self.font.render(arrow_text, True, (80, 80, 80))
        screen.blit(arrow_surf, (self.rect.right - 20, self.rect.centery - 8))

        self.option_rects = []
        if self.is_open:
            for i, opt in enumerate(self.options):
                opt_rect = pygame.Rect(self.rect.x, self.rect.bottom + (i * self.rect.height), self.rect.width, self.rect.height)
                self.option_rects.append((opt_rect, opt, i))

                color = (190, 210, 240) if opt_rect.collidepoint(mouse_pos) else (245, 245, 245)
                pygame.draw.rect(screen, color, opt_rect)
                pygame.draw.rect(screen, (150, 150, 150), opt_rect, width=1)

                opt_surf = self.font.render(opt, True, (30, 30, 30))
                opt_text_rect = opt_surf.get_rect(center=opt_rect.center)
                screen.blit(opt_surf, opt_text_rect)
