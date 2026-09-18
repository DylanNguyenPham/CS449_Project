import pygame
from Classes import Button

pygame.init()

# Window settings
BG_WIDTH = 800
BG_HEIGHT = 600

# ==========================================
# CURRENT STATE VARIABLES
# ==========================================
current_bg_color = (245, 245, 245)     # Default Light Gray
current_text_color = (30, 30, 30)      # Default Dark Text
current_peg_color = (30, 130, 230)     # Default Blue

# Dot settings
DOT_RADIUS = 20
DOT_SPACING = 60
DOT_COLOR_HOLE = (200, 200, 200)
BOARD_START_X = 80
BOARD_START_Y = 80

# Fonts
font_title = pygame.font.SysFont(None, 48)
font_label = pygame.font.SysFont(None, 32)
font_button = pygame.font.SysFont(None, 24)

# 7x7 English Board Layout
board_layout = [
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 2, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0]
]

# ==========================================
# BUTTONS
# ==========================================
_b_w, _b_h = 140, 35
_b_x = BG_WIDTH - _b_w - 40
btn_text_c = (30, 30, 30)
btn_c = (230, 230, 230)
btn_hover = (190, 190, 190)

# Game Controls
new_game_btn = Button(_b_x, 130, _b_w, _b_h, "New Game", font_button, btn_text_c, btn_c, btn_hover)
replay_btn = Button(_b_x, 175, _b_w, _b_h, "Replay", font_button, btn_text_c, btn_c, btn_hover)

# Background Selectors
bg_red_btn = Button(_b_x, 250, _b_w, _b_h, "Red ", font_button, (255,255,255), (200, 50, 50), (220, 80, 80))
bg_blue_btn = Button(_b_x, 295, _b_w, _b_h, "Blue ", font_button, (255,255,255), (50, 150, 255), (80, 180, 255))
bg_black_btn = Button(_b_x, 340, _b_w, _b_h, "Black ", font_button, (255,255,255), (40, 40, 40), (70, 70, 70))

# Peg Selectors
peg_blue_btn = Button(_b_x, 415, _b_w, _b_h, "Blue ", font_button, (255,255,255), (30, 130, 230), (60, 160, 255))
peg_green_btn = Button(_b_x, 460, _b_w, _b_h, "Green ", font_button, (255,255,255), (40, 200, 80), (70, 230, 110))

buttons = [new_game_btn, replay_btn, bg_red_btn, bg_blue_btn, bg_black_btn, peg_blue_btn, peg_green_btn]

# ==========================================
# FUNCTIONS
# ==========================================
def draw_text_right_aligned(screen, text, font, color, y_pos):
    surface = font.render(text, True, color)
    x_pos = BG_WIDTH - surface.get_width() - 40
    screen.blit(surface, (x_pos, y_pos))

def draw_ui(screen, mouse_pos):
    draw_text_right_aligned(screen, "Peg Solitaire", font_title, current_text_color, 40)
    draw_text_right_aligned(screen, "Board size: 7", font_label, current_text_color, 80)
    
    # Category Labels
    draw_text_right_aligned(screen, "Backgrounds", font_button, current_text_color, 225)
    draw_text_right_aligned(screen, "Peg Colors", font_button, current_text_color, 390)

    for button in buttons:
        button.draw(screen, mouse_pos)

def draw_board(screen):
    for row in range(7):
        for col in range(7):
            val = board_layout[row][col]
            if val != 0:
                x = BOARD_START_X + (col * DOT_SPACING)
                y = BOARD_START_Y + (row * DOT_SPACING)
                
                if val == 1:
                    pygame.draw.circle(screen, current_peg_color, (x, y), DOT_RADIUS)
                    pygame.draw.circle(screen, (30, 30, 30), (x, y), DOT_RADIUS, 2)
                else:
                    pygame.draw.circle(screen, DOT_COLOR_HOLE, (x, y), DOT_RADIUS)
                    pygame.draw.circle(screen, (150, 150, 150), (x, y), DOT_RADIUS, 2)

def handle_event(event):
    global current_bg_color, current_text_color, current_peg_color
    for button in buttons:
        if button.is_clicked(event):
            if button == bg_red_btn:
                current_bg_color, current_text_color = (200, 50, 50), (255, 255, 255)
            elif button == bg_blue_btn:
                current_bg_color, current_text_color = (50, 150, 255), (255, 255, 255)
            elif button == bg_black_btn:
                current_bg_color, current_text_color = (30, 30, 30), (255, 255, 255)
            elif button == peg_blue_btn:
                current_peg_color = (30, 130, 230)
            elif button == peg_green_btn:
                current_peg_color = (40, 200, 80)
            else:
                print(f"{button.text} clicked")